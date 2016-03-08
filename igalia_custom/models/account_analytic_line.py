# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def _prepare_cost_invoice_line(self, invoice_id, product_id, uom, user_id,
                                   factor_id, account, analytic_lines,
                                   journal_type, data):
        res = super(AccountAnalyticLine, self)._prepare_cost_invoice_line(
            invoice_id=invoice_id, product_id=product_id, uom=uom,
            user_id=user_id, factor_id=factor_id, account=account,
            analytic_lines=analytic_lines, journal_type=journal_type,
            data=data)
        if res.get('account_id', False):
            acc = self.env['account.account'].browse(res.get('account_id'))
            acc = account.partner_id.property_account_position.map_account(acc)
            res['account_id'] = acc.id
        return res
