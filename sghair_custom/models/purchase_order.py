# Copyright 2019 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    logo_id = fields.Many2one(
        string="Logo",
        comodel_name="res.company.logo",
        default=lambda self: self.env["res.company.logo"].get_default_logo(),
    )
