# Copyright 2019 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    logo_id = fields.Many2one(
        string="Logo",
        comodel_name="res.company.logo",
        default=lambda self: self.env["res.company.logo"].get_default_logo(),
    )

    @api.model
    def create(self, vals):
        if self.env.context.get("sale_order", False):
            vals["logo_id"] = self.env.context.get("sale_order").logo_id.id
        return super().create(vals)
