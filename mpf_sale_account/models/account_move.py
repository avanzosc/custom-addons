# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    opportunity_id = fields.Many2one(
        comodel_name="crm.lead",
        string="Opportunity",
        check_company=True,
        domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False),"
        " ('company_id', '=', company_id)]",
    )
    lead_type_id = fields.Many2one(
        string="Type",
        comodel_name="type",
        related="opportunity_id.leadType",
        store=True,
    )
    lead_brand_id = fields.Many2one(
        string="Brand", comodel_name="brand", related="opportunity_id.brand", store=True
    )
