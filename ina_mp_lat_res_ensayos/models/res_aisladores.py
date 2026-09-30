# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResAisladores(models.Model):
    _name = "res.aisladores"
    _description = "LAT Resultados de ensayo de Aisladores"
    _inherit = ["ina.lat.lot.mixin"]

    name = fields.Float(string="Número", digits=(15, 0))
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    tension = fields.Integer()
    rechazado = fields.Boolean(default=False)
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    notas = fields.Char()
