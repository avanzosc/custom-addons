# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tools import html2plaintext


class AccountMove(models.Model):
    _inherit = "account.move"

    def has_narration(self):
        self.ensure_one()
        return bool(html2plaintext(self.narration or "").strip())
