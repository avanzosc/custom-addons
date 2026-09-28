# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    current_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Current Salesperson",
        readonly=True,
    )
    hlc_segment_id = fields.Many2one(
        comodel_name="partner.segment",
        string="Segment",
        readonly=True,
    )

    @api.model
    def _select(self) -> SQL:
        return SQL(
            "%s, move_partner.user_id AS current_user_id, "
            "move_partner.hlc_segment_id AS hlc_segment_id",
            super()._select(),
        )

    @api.model
    def _from(self) -> SQL:
        return SQL(
            "%s LEFT JOIN res_partner move_partner "
            "ON move_partner.id = move.partner_id",
            super()._from(),
        )
