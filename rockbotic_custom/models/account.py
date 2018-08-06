# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_exempt = fields.Boolean(
        string='Tax exempt', default=False)


class AccountAnalyticAccont(models.Model):
    _inherit = 'account.analytic.account'

    recurring_first_day = fields.Boolean(default=True)
    recurring_last_day = fields.Boolean(default=False)

    @api.model
    def _prepare_invoice_data(self, contract):
        res = super(AccountAnalyticAccont,
                    self)._prepare_invoice_data(contract)
        if 'comment' in res and not res['comment']:
            del res['comment']
        return res

    @api.multi
    def name_get(self):
        if not self.env.context.get('only_name', False):
            return super(AccountAnalyticAccont, self).name_get()
        res = []
        for account in self:
            res.append((account.id, account.name))
        return res


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    literal_header_invoice = fields.Text(string='literal header invoice')
