# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    account_analytic_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        readonly=True,
    )

    @api.model
    def _select(self):
        return SQL(
            "%s, move.account_analytic_id AS account_analytic_id",
            super()._select(),
        )
