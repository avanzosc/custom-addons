# -*- coding: utf-8 -*-
# Copyright Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'

    @api.multi
    def write(self, values):
        if values.get('price_unit', False):
            for line in self.filtered(lambda x: x.analytic_account_id):
                vals = {'account_id': line.analytic_account_id.id,
                        'date': fields.Datetime.now(),
                        'user_id': self.env.uid,
                        'name': u"{}: {}".format(_('Price unit'),
                                                 line.price_unit)}
                self.env['account.analytic.account.historical'].create(vals)
        return super(AccountAnalyticInvoiceLine, self).write(values)
