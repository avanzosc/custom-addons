# -*- coding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class AccountAnalyticChart(models.TransientModel):
    _inherit = 'account.analytic.chart'

    @api.multi
    def analytic_account_chart_open_window2(self):
        analytic_obj = self.env['account.analytic.account']
        analyti_ids = analytic_obj.search([])
        field_names = ['debit', 'credit', 'balance']
        data = analyti_ids.with_context(
            from_date=self.from_date,
            to_date=self.to_date)._debit_credit_bal_qtty(field_names, {})
        delete = []
        for key, val in data.items():
            if val['balance'] == 0:
                delete.append(key)
        for del_key in delete:
            del data[del_key]
        action = self.env.ref('account.action_account_analytic_account_tree2')
        action_dict = action.read()[0] if action else {}
        action_dict.update({'domain': "[('id','in',{})]".format(data.keys()),
                            'context': {'from_date': self.from_date,
                                        'to_date': self.to_date, },
                            'view_type': 'form'})
        return action_dict
