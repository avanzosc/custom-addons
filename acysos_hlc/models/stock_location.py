from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    for_stock_b2b = fields.Boolean(string="For B2B stock control")
