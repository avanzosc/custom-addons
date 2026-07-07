# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResEnlaces(models.Model):
    _name = "res.enlaces"
    _description = "LAT Resultados de ensayo de Enlaces"

    name = fields.Char(string="Numero Serie")
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    tension = fields.Integer(string="Tension de Ensayo")
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    notas = fields.Char()
