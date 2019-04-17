# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.model
    def _create_invoices(self, inv_values, sale_id):
        inv_id = super(SaleAdvancePaymentInv,
                       self)._create_invoices(inv_values, sale_id)
        inv = self.env['account.invoice'].browse(inv_id)
        inv.sale_order_id = sale_id
        return inv_id
