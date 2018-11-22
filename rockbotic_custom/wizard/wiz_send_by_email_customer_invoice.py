# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizSendByEmailCustomerInvoice(models.TransientModel):
    _name = 'wiz.send.by.email.customer.invoice'
    _description = 'Wizard for send email to customer'

    @api.multi
    def button_send_email(self):
        invoice_obj = self.env['account.invoice']
        for invoice in invoice_obj.browse(
            self.env.context.get('active_ids')).filtered(
                lambda l: l.type == 'out_invoice' and l.state == 'open'):
            invoice.send_by_email_customer_invoice()
