# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResBasesCutout(models.Model):
    _name = "res.basescutout"
    _description = "LAT Resultados de ensayo de bases y cutout"

    num_serie = fields.Float(string="Numero de Serie", index=True, digits=(15, 0))
    name = fields.Float(string="Numero", digits=(15, 0))
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    notas = fields.Char()
