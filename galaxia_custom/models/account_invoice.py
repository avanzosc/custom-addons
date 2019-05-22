# -*- coding: utf-8 -*-
# © 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _
import time


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        if 'from_automatic_recurring_invoice' in self.env.context:
            invoice_line = invoice.invoice_line.filtered(
                lambda x: x.account_analytic_id)
            if invoice_line:
                line = invoice_line[0]
                if line.account_analytic_id.recurring_invoice_incidence_ids:
                    account = line.account_analytic_id
                    price = 0.0
                    notes = False
                    for inci in account.recurring_invoice_incidence_ids:
                        if (invoice.date_invoice >= inci.from_date and
                                invoice.date_invoice <= inci.to_date):
                            price += inci.price
                            if line.name:
                                notes = (
                                    line.name if not notes else
                                    u"{}, {}".format(notes, line.name))
                    new_price = line.price_unit + price
                    line.price_unit = new_price
                    if notes:
                        line.invoice_id.comment = notes
        return invoice
