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

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class InaelEndesa(models.Model):
    """Histórico de entregas de Endesa de v10, solo para consulta.

    Los campos que en v10 se calculaban desde la OV se guardan tal cual
    estaban: ya no se crean líneas ni se recalculan.
    """

    _name = "inael.endesa"
    _description = "Endesa de OV"

    sale_line_id = fields.Many2one(comodel_name="sale.order.line", string="Línea OV")
    sale_id = fields.Many2one(comodel_name="sale.order", string="O.V.")
    codigo = fields.Char("Código Endesa")
    pedido = fields.Char("Pedido Endesa")
    cantidad = fields.Float()
    entregado = fields.Float("Q.Entregado")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Destino")
    # Nombre de la dirección de entrega, sin la empresa delante.
    partner_id_corto = fields.Char("Destino Corto", related="partner_id.name")
    default_code = fields.Char("Referencia")
    contrato = fields.Char("Nº Contrato")
    fecha_planifica = fields.Datetime("Fecha Planificada")
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
    revisar = fields.Boolean()
    entrega_check = fields.Boolean("Entregado")
    of = fields.Char("OF")
    fecha_fabricacion = fields.Datetime("Fecha Fabricación")
    # Sin guardar: depende de la fecha de hoy.
    color_fecha = fields.Selection(
        [
            ("rojo", "Rojo"),
            ("naranja", "Naranja"),
            ("amarillo", "Amarillo"),
            ("ok", "OK"),
        ],
        compute="_compute_color_fecha",
    )

    @api.depends("fecha_necesidad", "estado")
    def _compute_color_fecha(self):
        hoy = fields.Date.context_today(self)
        for rec in self:
            color = "ok"
            if rec.fecha_necesidad and rec.estado != "QA":
                fecha = rec.fecha_necesidad.date()
                if fecha <= hoy:
                    color = "rojo"
                elif fecha <= hoy + relativedelta(days=7):
                    color = "naranja"
                elif fecha <= hoy + relativedelta(days=15):
                    color = "amarillo"
            rec.color_fecha = color
