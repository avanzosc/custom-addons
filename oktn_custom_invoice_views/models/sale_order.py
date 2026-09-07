# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        values = super()._prepare_invoice()
        if self.project_id and self.project_id.account_id:
            values["account_analytic_id"] = self.project_id.account_id.id
        return values
