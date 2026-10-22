#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class InaelEndesa(models.Model):
    _name = "inael.endesa"
    _description = "Endesa de OV"

    @api.depends("fecha_necesidad", "estado")
    def _compute_color_fecha(self):
        for r in self:
            r.color_fecha = "ok"

            if not r.fecha_necesidad or r.estado == "QA":
                continue

            hoy = fields.Date.context_today(r)

            fecha = r.fecha_necesidad.date()

            if fecha <= hoy:
                r.color_fecha = "rojo"
            elif fecha <= hoy + relativedelta(days=7):
                r.color_fecha = "naranja"
            elif fecha <= hoy + relativedelta(days=15):
                r.color_fecha = "amarillo"
            else:
                r.color_fecha = "ok"

    @api.model
    def cron_actualizar_colores(self):
        records = self.search([("estado", "!=", "QA")])
        self.env.add_to_compute(self._fields["color_fecha"], records)
        records._recompute_recordset(["color_fecha"])

    color_fecha = fields.Selection(
        [
            ("rojo", "Rojo"),
            ("naranja", "Naranja"),
            ("amarillo", "Amarillo"),
            ("ok", "OK"),
        ],
        compute="_compute_color_fecha",
        store=True,
    )

    @api.depends("cantidad", "entregado")
    def _compute_entregado(self):
        for rec in self:
            rec.entrega_check = rec.entregado >= rec.cantidad

    sale_line_id = fields.Many2one(comodel_name="sale.order.line", string="Linea OV")
    sale_id = fields.Many2one(comodel_name="sale.order", string="O.V.")
    codigo = fields.Char("Codigo Endesa")
    pedido = fields.Char("Pedido Endesa")
    cantidad = fields.Float(
        "Cantidad", related="sale_line_id.product_uom_qty", store=True
    )
    entregado = fields.Float(
        "Q.Entregado", related="sale_line_id.qty_delivered", store=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Destino",
        related="sale_id.partner_shipping_id",
        store=True,
    )
    partner_id_corto = fields.Char("Destino Corto", compute="_compute_destino")
    default_code = fields.Char("Referencia")
    contrato = fields.Char("Nº Contrato")
    fecha_planifica = fields.Datetime(
        "Fecha Planificada", compute="_compute_fecha_planifica", store=True
    )
    fecha_necesidad = fields.Datetime()
    ns = fields.Char("N/S")
    estado = fields.Selection(
        [
            ("PDP", "PDP"),
            ("PDI", "PDI"),
            ("CSV", "CSV"),
            ("QA", "QA"),
        ],
    )
    idcal = fields.Char("ID Cal")
    entrega = fields.Boolean("Enviado")
    estado_linea = fields.Selection(string="Estado Linea", related="sale_line_id.state")
    revisar = fields.Boolean()
    entrega_check = fields.Boolean(
        "Entregado", compute="_compute_entregado", store=True
    )
    of = fields.Char("OF")
    fecha_fabricacion = fields.Datetime(
        compute="_compute_fecha_fabricacion", store=True
    )

    @api.depends("fecha_planifica")
    def _compute_fecha_fabricacion(self):
        for rec in self:
            if rec.fecha_planifica:
                rec.fecha_fabricacion = rec.fecha_planifica - timedelta(days=7)
            else:
                rec.fecha_fabricacion = False

    @api.onchange("fecha_necesidad")
    def _onchange_fecha_necesidad(self):
        if not self.fecha_necesidad:
            return

        self.revisar = True

    @api.depends("sale_id.fecha_confirmada")
    def _compute_fecha_planifica(self):
        for rec in self:
            rec.fecha_planifica = rec.sale_id.fecha_confirmada

    @api.depends("partner_id")
    def _compute_destino(self):
        for record in self:
            record.partner_id_corto = False
            if record.partner_id:
                nombre = record.partner_id.name
                record.partner_id_corto = (
                    (nombre[:20] + "..") if len(nombre) > 20 else nombre
                )

    def actualizar_endesa(self):
        self.env.flush_all()
        sql = """
            SELECT a.id            AS ov,
                   d.default_code  AS refer,
                   b.id            AS bline_id,
                   h.cod_cia       AS cod_cia
              FROM sale_order a
              JOIN sale_order_line b   ON b.order_id = a.id
              JOIN product_product d   ON d.id = b.product_id
              JOIN product_template f  ON f.id = d.product_tmpl_id
              JOIN product_homologa h  ON h.product_id = b.product_id
             WHERE a.state = 'sale'
               AND a.locked IS NOT TRUE
               AND a.date_order >= '2025-01-01'
               AND f.type != 'service'
               AND a.partner_id in (3030, 7740, 7603)
               AND h.cia = 1
        """
        self.env.cr.execute(sql)
        res = self.env.cr.dictfetchall()
        for r in res:
            w_refe = r["refer"]
            w_ov = r["ov"]
            w_sale_line_id = r["bline_id"]
            w_cod_cia = r["cod_cia"]

            ov = self.env["sale.order"].browse(w_ov)
            val = {
                "sale_line_id": w_sale_line_id,
                "sale_id": ov.id,
                "codigo": w_cod_cia,
                "pedido": ov.client_order_ref,
                "default_code": w_refe,
                "contrato": ov.origin,
            }

            endesa_ids = self.env["inael.endesa"].search(
                [("sale_id", "=", ov.id), ("sale_line_id", "=", w_sale_line_id)]
            )
            if not endesa_ids:
                self.env["inael.endesa"].create(val)

        return True

    def action_actualizar_entregas(self):
        self.actualizar_endesa()
        self.cron_actualizar_colores()
        return {"type": "ir.actions.client", "tag": "reload"}
