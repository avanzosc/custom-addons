# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductRevision(models.Model):
    _name = "product.revision"
    _description = "product revision"

    product_id = fields.Many2one(comodel_name="product.template", string="Revision")
    fecha = fields.Date()
    observacion = fields.Char(string="Observaciones")
    revision = fields.Char(help="Codigo de la revision", size=12)
