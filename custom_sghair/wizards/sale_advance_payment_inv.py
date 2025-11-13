# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, sale_orders):
        self.sale_order_ids.ensure_one()
        self = self.with_company(self.company_id)
        so = self.sale_order_ids
        res = super(
            SaleAdvancePaymentInv, self.with_context(sale_order=so)
        )._create_invoice(sale_orders)
        return res
