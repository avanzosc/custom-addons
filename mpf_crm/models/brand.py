# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class Brand(models.Model):
    _name = "brand"
    _description = "Brand"

    name = fields.Char("Description", required=True, index=True)
    lead_ids = fields.One2many(
        string="Assigned leads", comodel_name="crm.lead", inverse_name="brand_id"
    )
