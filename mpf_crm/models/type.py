# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class Type(models.Model):
    _name = "type"
    _description = "Crm Lead Type"

    name = fields.Char("Description", required=True, index=True)
    lead_ids = fields.One2many(
        string="Assigned leads", comodel_name="crm.lead", inverse_name="lead_type_id"
    )
