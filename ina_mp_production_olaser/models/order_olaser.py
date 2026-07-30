# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError


class OrderoLaser(models.Model):
    _name = "order.olaser"
    _inherit = ["mail.thread"]  # Para poner historia abajo
    _description = "Orden de OLaser"

    @api.depends("terminado")
    def _compute_tiempo_realizado(self):
        for r in self:
            r.tiempo_realizado = r.terminado * r.tiempo

    @api.depends(
        "listas_ids.cantidad_consumo_total",
        "listas_ids.tiempo_total",
        "peso_mp",
        "cantidad",
    )
    def _compute_cantidades(self):
        for r in self:
            w_c = sum(x.cantidad_consumo_total for x in r.listas_ids)
            w_t = sum(z.tiempo_total for z in r.listas_ids)
            r.cantidad_consumo_total = r.peso_mp * r.cantidad
            r.cantidad_consumo_real = w_c * r.cantidad
            desperdicio = (r.cantidad * r.peso_mp) - r.cantidad_consumo_real
            r.desperdicio = max(desperdicio, 0)
            r.tiempo_total = w_t
            r.tiempo = (w_t / r.cantidad) if r.cantidad else 0

    @api.depends("rechazos_ids.procesado", "state")
    def _compute_rechazos_ptes(self):
        for r in self:
            tiene_pendientes = any(not c.procesado for c in r.rechazos_ids)
            r.rechazos_ptes = (
                False if r.state in ("done", "cancel") else tiene_pendientes
            )

    @api.onchange("cantidad", "listas_ids")
    def onchange_cantidad(self):
        for r in self:
            for line in r.listas_ids:
                line.cantidad_chapa_total = r.cantidad * line.cantidad_chapa
                line.cantidad_consumo_total = (
                    line.cantidad_chapa * line.cantidad_consumo
                )
                line.tiempo_total = line.cantidad_chapa_total * line.tiempo_ud
                line.peso_gas_total = line.peso_gas * line.cantidad_chapa_total

    name = fields.Char(string="Num. Orden", required=True, default="/", readonly=True)
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("cancel", "Cancelado"),
            ("confirmado", "Confirmado"),
            ("proceso", "En Proceso"),
            ("done", "Terminado"),
        ],
        default="draft",
        string="Estado",
        copy=False,
        tracking=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Materia Prima",
        store=True,
        domain=[("tipo_comp_fab", "=", "comprado")],
        required=True,
    )
    cantidad = fields.Float(digits=(9, 2), default=0, required=True)
    comunicado = fields.Float(
        string="Qt. Comunicada", digits=(9, 2), default=0, copy=False
    )
    terminado = fields.Float(
        string="Qt. Terminada", digits=(9, 2), default=0, copy=False
    )
    date = fields.Datetime(
        string="Fecha", required=True, default=fields.Datetime.now, copy=False
    )
    tiempo = fields.Float(
        string="Tiempo chapa",
        default=0,
        compute="_compute_cantidades",
        help="Tiempo x Chapa en Minutos",
    )
    location_id = fields.Many2one(
        comodel_name="stock.location", string="Ubicacion Laser", required=True
    )  # 1844 = Laser
    listas_ids = fields.One2many(
        comodel_name="order.olaser.lista",
        inverse_name="olaser_id",
        string="Referencias Nesting",
        readonly=True,
    )
    lista_olaser_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="lista_olaser_id",
        string="Lista Material",
        copy=False,
    )
    olaser_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="olaser_id",
        string="Orden Laser-MP ",
        copy=False,
    )
    laser_tiempos_ids = fields.One2many(
        comodel_name="order.olaser.tiempos",
        inverse_name="laser_tiempos_id",
        string="O.Laser",
    )
    cantidad_consumo_total = fields.Float(
        string="Cantidad consumo total",
        compute="_compute_cantidades",
        digits=(9, 2),
        default=0,
    )
    cantidad_consumo_real = fields.Float(
        string="Cantidad consumo real",
        compute="_compute_cantidades",
        digits=(9, 2),
        default=0,
    )
    tiempo_total = fields.Float(
        string="Tiempo chapa total",
        compute="_compute_cantidades",
        default=0,
        help="Tiempo Total  en Minutos",
    )
    tiempo_realizado = fields.Float(
        string="Tiempo chapa realizado",
        compute="_compute_tiempo_realizado",
        help="Tiempo Realizado x Chapa en Minutos",
    )
    desperdicio = fields.Float(
        compute="_compute_cantidades", digits=(9, 2), default=0, copy=False
    )
    peso_mp = fields.Float(string="Peso Kgs", digits=(9, 2), required=True)
    es_retal = fields.Boolean(
        string="Es un retal",
        default=False,
        help="Si se marca, no se produciran movimientos de Mat. Prima",
    )
    product_gas_id = fields.Many2one(
        comodel_name="product.product", string="Gas Utilizado"
    )
    rechazos_ids = fields.One2many(
        comodel_name="order.olaser.rechazo",
        inverse_name="olaser_id",
        string="Rechazos en laser",
    )
    rechazos_ptes = fields.Boolean(
        string="Rechazos Pendientes", compute="_compute_rechazos_ptes", default=False
    )
    _sql_constraints = [
        (
            "order_olaser_unique_code",
            "UNIQUE (name)",
            "El numero de orden debe ser unico!",
        ),
    ]

    @api.onchange("product_id")
    def onchange_product_id(self):
        for r in self:
            r.peso_mp = r.product_id.weight
            r.product_gas_id = r.product_id.product_gas_id.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("cantidad", 0) <= 0:
                raise exceptions.UserError(_("La cantidad tiene que ser mayor que 0."))
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code("order.olaser")
        return super().create(vals_list)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = self.env["ir.sequence"].next_by_code("order.olaser")
        return super().copy(default)

    def unlink(self):
        for record in self:
            if record.state != "cancel":
                raise exceptions.UserError(
                    _("No se pueden borrar registros. Tienes que Cancelar.")
                )
        return super().unlink()

    def action_duplicar(self):
        wid_1 = self.id
        wid_2 = self.copy()
        lista_obj = self.env["order.olaser.lista"]
        duplica_ids = self.env["order.olaser"].browse(wid_1)
        for s in duplica_ids:
            wid_2.peso_mp = s.peso_mp
            for r in s.listas_ids:
                val = {
                    "olaser_id": wid_2.id,
                    "product_id": r.product_id.id,
                    "cantidad_chapa": r.cantidad_chapa,
                    "cantidad_chapa_total": r.cantidad_chapa_total,
                    "cantidad_consumo": r.cantidad_consumo,
                    "cantidad_consumo_total": r.cantidad_consumo_total,
                    "tiempo_ud": r.tiempo_ud,
                    "tiempo_total": r.tiempo_total,
                    "peso_gas": r.peso_gas,
                    "peso_gas_total": r.peso_gas_total,
                    "plano": r.product_id.plano,
                }
                lista_obj.create(val)
        value = {
            "name": _("Orden Laser"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "order.olaser",
            "res_id": wid_2.id,
        }
        return value

    def action_cancelar(self):
        if any(prep.comunicado > 0 for prep in self):
            raise UserError(_("No puede cancelar cuando se ha comunicado cantidades."))
        for move in self.lista_olaser_ids:
            if move.state in ("done", "cancel"):
                continue  # los hechos paso de ellos.
            move.action_cancel()  # ejecuto
        for movi in self:
            # Busco el producto terminado, para cancelar lo que queda pendiente
            termi_moves = movi.olaser_ids.filtered(
                lambda x: x.state not in ("done", "cancel")
            )
            # Cancelo el movimiento de productos terminados
            (termi_moves).action_cancel()
        self.write({"state": "cancel"})

    def action_cerrar(self):
        self._revertir_moves()
        self.write({"state": "done"})

    def action_procesar(self):
        self.procesar_mp()
        self.procesar_lineas()

    def procesar_comunicados(self):
        ot_obj = self.env["order.olaser"]
        cond = [("comunicado", ">", 0), ("state", "=", "proceso")]
        ot_ids = ot_obj.search(cond)
        for r in ot_ids:
            # print " @@@@ ", r.name
            r.procesar_mp()
            r.procesar_lineas()
        return True

    def _revertir_moves(self):
        for move in self.lista_olaser_ids:
            if move.state in ("done", "cancel"):
                # los hechos paso de ellos.
                continue
            # confirmo
            move.action_cancel()
        for movi in self:
            #  Busco el producto terminado, para cancelar lo que queda pendiente
            termi_moves = movi.olaser_ids.filtered(
                lambda x: x.state not in ("done", "cancel")
            )
            # Cancelo el movimiento de productos terminados.
            (termi_moves).action_cancel()

    def action_validar(self):
        if not self.listas_ids:
            raise exceptions.UserError(
                _("No puedes validar sin tener una distribucion.")
            )
        for orden in self:
            if orden.state != "draft":
                raise exceptions.UserError(
                    _("No puedes validar una orden que no este en modo Borrador.")
                )
        self._generate_moves()
        self.action_assign()  # Reservamos stock
        self.write({"state": "confirmado"})

    def action_assign(self):
        for r in self.olaser_ids:
            move_to_assign = r.filtered(
                lambda x: x.state in ("confirmed", "waiting", "assigned")
            )
            move_to_assign.action_assign()
        return True

    def action_procesar_rechazo(self):
        sw = 0
        for lin in self.rechazos_ids:
            if lin.procesado:
                continue
            sw += 1
            val = {
                "sequence": sw,
                "name": self.name,
                "date": self.date,
                "date_expected": self.date,
                "product_id": lin.product_id.id,
                "product_uom": lin.product_id.uom_id.id,
                "product_uom_qty": lin.cantidad,
                "location_id": self.location_id.id,
                "location_dest_id": 4,  # Ubicacion desecho   virtual/Desechado
                "move_dest_id": False,
                "procurement_id": False,
                "lista_olaser_id": self.id,
                "origin": self.name,
            }
            move = self.env["stock.move"].create(val)
            move.action_confirm()
            move.action_done()
            lin.write({"procesado": True})
        return move

    def action_view_stock_moves(self):
        products = self.mapped("olaser_ids")
        products += self.mapped("lista_olaser_ids")
        action = self.env.ref("stock.act_product_stock_move_open").read()[0]
        if products:
            action["context"] = {"default_product_id": products.ids[0]}
        action["domain"] = [("id", "in", products.ids)]
        return action

    def _generate_moves(self):
        ubicacion = self.env["stock.location"]
        w_fabrica_location = ubicacion.search(
            [("usage", "=", "production")], limit=1
        ).id  # location_id  7 ORDEN FABRICA
        for production in self:
            production._genera_final_moves(w_fabrica_location)
            production._genera_lineas_moves(w_fabrica_location)
        return True

    def _genera_final_moves(self, w_fabrica_location):
        if self.es_retal:
            return
        # MATERIA PRIMA
        val = {
            "name": self.name,
            "date": self.date,
            "date_expected": self.date,
            "product_id": self.product_id.id,
            "product_uom": self.product_id.uom_id.id,
            "product_uom_qty": self.cantidad * self.peso_mp,
            "location_id": self.location_id.id,
            "location_dest_id": w_fabrica_location,
            "move_dest_id": False,
            "procurement_id": False,
            "olaser_id": self.id,
            "origin": self.name,
            "price_unit": self.product_id.standard_price,
        }
        move = self.env["stock.move"].create(val)
        move.action_confirm()
        # GAS
        # ANULO EL TEMA DEL GAS---> PARA QUE NO FUNCIONE PORQUE SE AJUSTA A FINAL DE MES
        w_can_gas = 0
        for lin in self.listas_ids:
            w_can_gas += lin.peso_gas_total
        val = {
            "name": self.name,
            "date": self.date,
            "date_expected": self.date,
            "product_id": self.product_gas_id.id,
            "product_uom": self.product_gas_id.uom_id.id,
            "product_uom_qty": w_can_gas,
            "location_id": self.location_id.id,
            "location_dest_id": w_fabrica_location,
            "move_dest_id": False,
            "procurement_id": False,
            "olaser_id": self.id,
            "origin": self.name,
            "price_unit": self.product_gas_id.standard_price,
        }
        # anulo move = self.env["stock.move"].create(val)
        # anulo move.action_confirm()
        return move

    def _genera_lineas_moves(self, w_fabrica_location):
        sw = 0
        for lin in self.listas_ids:
            sw += 1
            val = {
                "sequence": sw,
                "name": self.name,
                "date": self.date,
                "date_expected": self.date,
                "product_id": lin.product_id.id,
                "product_uom": lin.product_id.uom_id.id,
                "product_uom_qty": lin.cantidad_chapa_total,
                "location_id": w_fabrica_location,
                "location_dest_id": self.location_id.id,
                "move_dest_id": False,
                "procurement_id": False,
                "olaser_id": self.id,
                "lista_olaser_id": self.id,
                "origin": self.name,
                "olaser_linea_id": lin.id,
                # "cantidad_ldm":lin.cantidad_chapa_total,
            }
            move = self.env["stock.move"].create(val)
            move.action_confirm()
        return move

    def procesar_mp(self):
        # tipo=1 para consumir  tipo=2 para alta en inventario producto fabricado
        if self.es_retal:
            return
        w_cant = self.comunicado * self.peso_mp
        w_can_gas = 0
        for lin in self.listas_ids:
            w_can_gas += lin.peso_gas_total
        for move in self.olaser_ids:
            if move.state in ("done", "cancel"):
                continue  # los hechos paso de ellos.
            if move.product_id == self.product_id:
                if self.terminado + self.comunicado == self.cantidad:
                    move.action_done()
                else:
                    nuevo_move = move.dividir(w_cant)
                    nuevo_move.action_done()
            elif move.product_id == self.product_gas_id:
                if self.terminado + self.comunicado == self.cantidad:
                    move.action_done()
                else:
                    # Calculo la cantidad de gas a consumir
                    w_cant = self.comunicado * w_can_gas / self.cantidad
                    nuevo_move = move.dividir(w_cant)
                    nuevo_move.action_done()

    def procesar_lineas(self):
        # tipo=1 para consumir  tipo=2 para alta en inventario producto fabricado
        w_comun = self.comunicado
        w_termi = self.terminado
        for lin in self.listas_ids:
            qty = 0
            moves_ids = self.lista_olaser_ids.filtered(
                lambda o, lin=lin: o.product_id == lin.product_id
            )
            for move in moves_ids:
                if move.state in ("done", "cancel"):
                    continue  # los hechos paso de ellos.
                qty = lin.cantidad_chapa * w_comun
                if move.product_uom_qty == qty:
                    move.action_done()
                else:
                    nuevo_move = move.dividir(qty)
                    nuevo_move.action_done()

            val = {"cantidad_chapa_termi": lin.cantidad_chapa_termi + qty}
            lin.write(val)  # grabo valores en la linea
            val = {
                "comunicado": 0,
                "terminado": w_termi + w_comun,
                "state": "proceso",
            }
            self.write(val)  # grabo valores en la olaser
