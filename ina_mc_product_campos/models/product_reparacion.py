# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductReparacion(models.Model):
    _name = "product.reparacion"
    _description = "product reparacion"

    product_id = fields.Many2one(
        comodel_name="product.template", string="producto de reparacion"
    )
    material_id = fields.Many2one(comodel_name="product.product", string="Material")
    cantidad = fields.Float(digits=(9, 2))
