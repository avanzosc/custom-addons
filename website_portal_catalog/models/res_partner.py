from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    send_catalog_id = fields.Many2one("product.catalog.web", "Send catalog")
