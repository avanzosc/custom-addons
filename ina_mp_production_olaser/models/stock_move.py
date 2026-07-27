# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    olaser_id = fields.Many2one(
        comodel_name="order.olaser", string="Orden Laser (Chapa MP )"
    )
    lista_olaser_id = fields.Many2one(
        comodel_name="order.olaser", string="Lista de Materiales"
    )
    olaser_retal_control = fields.Boolean(string="Tiene retal control")
    olaser_linea_id = fields.Many2one(
        comodel_name="order.olaser.lista", string="Orden Laser Linea"
    )
