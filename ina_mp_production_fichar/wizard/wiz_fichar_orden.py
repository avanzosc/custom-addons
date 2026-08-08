# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Wizard huerfano: se abria desde hr.employee.action_entrada_salida /
# action_fichar_nueva, que ahora estan comentados (el fichaje real ya no
# pasa por aqui). Se mantiene el modelo/vista y la logica original queda
# comentada solo como referencia.
from odoo import api, fields, models


class WizFicharOrden(models.TransientModel):
    _name = "wiz.fichar.orden"
    _description = "Wizard Fichar Orden"

    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
        string="Orden de Trabajo",
        domain="[('workcenter_id', '=', centro_puesto), "
        "('state', 'in', ('pending', 'ready', 'progress'))]",
    )
    production_id = fields.Many2one(
        comodel_name="mrp.production",
        string="Orden de producción",
        related="workorder_id.production_id",
    )
    repara_id = fields.Many2one(
        comodel_name="repair.order",
        string="Reparacion",
        domain="[('state', 'in', ('confirmed', 'under_repair', 'pteconfir'))]",
    )
    laser_id = fields.Many2one(
        comodel_name="order.olaser",
        string="Laser",
        domain="[('state', 'in', ('confirmado', 'proceso'))]",
    )
    improductivo = fields.Many2one(
        comodel_name="mrp.workcenter.productivity.loss",
        domain="[('loss_type', '=', 'availability')]",
    )
    tipo = fields.Selection(
        selection=[
            ("of", "Fabricacion"),
            ("repara", "Reparacion"),
            ("laser", "Laser"),
            ("impro", "Improductivo"),
        ],
        string="Tipo de Orden",
        default="of",
    )
    fichar_id = fields.Many2one(comodel_name="hr.employee", string="Fichar")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")
    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar", string="Puesto")
    centro_puesto = fields.Many2one(
        comodel_name="mrp.workcenter", string="Centro", related="puesto_id.centro_id"
    )
    tipo_fichar = fields.Selection(
        selection=[
            ("nueva", "Nueva Orden"),
            ("comunicar", "Comunicar Cantidad"),
            ("no", "Cantidad completa"),
        ],
        string="Tipo de Fichar",
        default="of",
    )
    refer_faltan = fields.Text("Faltan Referencias")
    cantidad = fields.Integer("Cantidad Aceptada")
    cantidad_rechazada = fields.Integer()
    datos_orden = fields.Text("Orden")
    datos_laser = fields.Text()

    # --- Logica operativa comentada: solo referencia, no se ejecuta. ---

    # @api.onchange("workorder_id")
    # def onchange_workorder_id(self):
    #     if self.workorder_id:
    #         p = self.workorder_id.product_id
    #         self.datos_orden = (
    #             "%s %s\nA producir: %s\nComunicada: %s\nProducida : %s"
    #             % (
    #                 p.default_code or "",
    #                 p.name or "",
    #                 self.workorder_id.qty_production,
    #                 self.workorder_id.aceptada + self.workorder_id.rechazada,
    #                 self.workorder_id.qty_produced,
    #             )
    #         )
    #     else:
    #         self.datos_orden = ""

    # @api.onchange("laser_id")
    # def onchange_laser_id(self):
    #     if self.laser_id:
    #         p = self.laser_id.product_id
    #         self.datos_laser = (
    #             "%s %s\nA producir: %s\nComunicada: %s\nProducida : %s"
    #             % (
    #                 p.default_code or "",
    #                 p.name or "",
    #                 self.laser_id.cantidad,
    #                 self.laser_id.comunicado,
    #                 self.laser_id.terminado,
    #             )
    #         )
    #     else:
    #         self.datos_laser = ""

    @api.model
    def default_get(self, var_fields):
        return super().default_get(var_fields)
        # if self.env.context.get("active_model", "") != "hr.employee":
        #     return {}
        # ids = self.env.context.get("active_ids", [])
        # if not ids:
        #     raise exceptions.UserError(_("Tienes que seleccionar 1 Empleado"))
        #
        # fichar_obj = self.env["hr.employee"]
        # w_usuario = self.env.user.id
        # puesto = self.env["hr.puesto.fichar"].search(
        #     [("user_id", "=", w_usuario)], limit=1
        # )
        #
        # for d in fichar_obj.browse(ids):
        #     wtipo_fichar = "nueva"
        #     wtipo = "of"
        #     wworkorder_id = wrepara_id = wlaser_id = False
        #
        #     if d.workorder_id or d.repara_id or d.laser_id:
        #         wtipo_fichar = "comunicar"
        #         if d.workorder_id:
        #             wtipo = "of"
        #             wworkorder_id = d.workorder_id
        #             if d.ot_qty_comunicada + d.ot_qty_producida >= d.ot_qty_aproducir:
        #                 wtipo_fichar = "no"
        #         elif d.laser_id:
        #             wtipo = "laser"
        #             wlaser_id = d.laser_id
        #             if d.la_qty_comunicada + d.la_qty_producida >= d.la_qty_aproducir:
        #                 wtipo_fichar = "no"
        #
        #     return {
        #         "fichar_id": d.id,
        #         "employee_id": d.id,
        #         "puesto_id": puesto.id if puesto else False,
        #         "tipo_fichar": wtipo_fichar,
        #         "tipo": wtipo,
        #         "workorder_id": wworkorder_id.id if wworkorder_id else False,
        #         "repara_id": wrepara_id.id if wrepara_id else False,
        #         "laser_id": wlaser_id.id if wlaser_id else False,
        #     }
        # return {}

    # def _get_ahora(self):
    #     ff = datetime.utcnow().replace(microsecond=0)
    #     tz = pytz.timezone("Europe/Madrid")
    #     ff_local = pytz.utc.localize(ff).astimezone(tz)
    #     ahora = ff
    #     if ff_local.minute >= 30 and ff_local.hour in (5, 13):
    #         ahora = ff.replace(minute=0, second=0) + timedelta(hours=1)
    #     return ahora

    def crear_orden(self):
        return True
        # ahora = self._get_ahora()
        # ids = self.env.context.get("active_ids", [])
        # fichar = self.env["hr.employee"]
        # ficha_ids = fichar.browse(ids)
        #
        # for r in ficha_ids:
        #     if (
        #         r.entrada_ultima
        #         and r.entrada_ultima.hour == 3
        #         and r.entrada_ultima.minute >= 30
        #     ):
        #         ahora = datetime.utcnow().replace(microsecond=0)
        #
        #     r.write({
        #         "workorder_id": False,
        #         "repara_id": False,
        #         "laser_id": False,
        #         "improductivo": False,
        #         "puesto_id": self.puesto_id.id,
        #     })
        #
        #     if self.tipo == "of":
        #         r.write({"tipo": "of", "workorder_id": self.workorder_id.id})
        #         fichar.grabar_fab(r, ahora)
        #     elif self.tipo == "repara":
        #         r.write({"tipo": "repara", "repara_id": self.repara_id.id})
        #         fichar.grabar_rep(r, ahora)
        #     elif self.tipo == "laser":
        #         r.write({"tipo": "laser", "laser_id": self.laser_id.id})
        #         fichar.grabar_las(r, ahora)
        #     elif self.tipo == "impro":
        #         r.write({"tipo": "impro", "improductivo": self.improductivo.id})
        #         fichar.grabar_imp(r, ahora)
        #
        # return True

    def comunicar_orden(self):
        return True
        # if not self.cantidad and not self.cantidad_rechazada:
        #     raise exceptions.UserError(_("No puedes comunicar sin cantidad."))
        #
        # ids = self.env.context.get("active_ids", [])
        # fichar = self.env["hr.employee"]
        # ficha_ids = fichar.browse(ids)
        #
        # for r in ficha_ids:
        #     if self.tipo == "of":
        #         w_cant1 = r.ot_qty_aproducir
        #         w_cant2 = r.ot_qty_comunicada + r.ot_qty_producida
        #         if w_cant2 >= w_cant1:
        #             raise exceptions.UserError(
        #                 _(
        #                     "La cantidad producida %s es igual o superior a la "
        #                     "cantidad a producir %s."
        #                 )
        #                 % (w_cant2, w_cant1)
        #             )
        #         fichar.comuni_fab(
        #             r, self.cantidad, self.cantidad_rechazada, self.refer_faltan,
        #             False, "procesada"
        #         )
        #     elif self.tipo == "laser":
        #         w_cant1 = r.la_qty_aproducir
        #         w_cant2 = r.la_qty_comunicada + r.la_qty_producida
        #         if w_cant2 >= w_cant1:
        #             raise exceptions.UserError(
        #                 _(
        #                     "La cantidad producida %s es igual o superior a la "
        #                     "cantidad a producir %s."
        #                 )
        #                 % (w_cant2, w_cant1)
        #             )
        #         nueva_cant = w_cant2 + self.cantidad
        #         if nueva_cant > w_cant1:
        #             raise exceptions.UserError(
        #                 _(
        #                     "La cantidad producida (%s) no puede ser mayor que "
        #                     "la cantidad a producir (%s)"
        #                 )
        #                 % (nueva_cant, w_cant1)
        #             )
        #         fichar.comuni_las(r, self.cantidad, False, False, "cerrada")
        # return True
