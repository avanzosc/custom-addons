# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    account_analytic_id = fields.Many2one(
        string="Analytic account", comodel_name="account.analytic.account", copy=False
    )
