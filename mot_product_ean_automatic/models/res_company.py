# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = "Res Company Inherit"

    country_company_code = fields.Char(string="Country Number Code")
    company_code = fields.Char(string="Company Number Code")
