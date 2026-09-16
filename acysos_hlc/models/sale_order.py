from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    catalog_id = fields.Many2one("product.catalog.web", string="Catalog")
