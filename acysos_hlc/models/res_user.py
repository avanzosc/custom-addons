from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    is_commercial = fields.Selection(
        selection=[("no", "No"), ("own", "Own clients"), ("all", "All clients")],
        default="no",
    )
