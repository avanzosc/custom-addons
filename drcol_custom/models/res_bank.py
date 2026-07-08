# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResBank(models.Model):
    _inherit = "res.bank"

    aba_routing_number = fields.Char(string="ABA Routing Number")
