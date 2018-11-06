# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_invoice_create(self, grouped=False, states=None,
                              date_invoice=False):
        invoice_id = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, states=states, date_invoice=date_invoice)
        invoice = self.env['account.invoice'].browse(invoice_id)
        invoice.sale_order_id = self.id
        return invoice_id
