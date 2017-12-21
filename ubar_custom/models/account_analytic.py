# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _domain_lot_id(self):
        today = fields.Date.today()
        accounts = self.env['account.analytic.account'].search(
            ['&', ('date_start', '<=', today), ('date', '>=', today)]).ids
        return ['|',
                ('account_analytic_ids', '=', False),
                ('account_analytic_ids', 'not in', accounts)]

    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot',
        domain=_domain_lot_id)
    quant_id = fields.Many2one(comodel_name='stock.quant', string='Quant',
                               domain="[('lot_id', '=', lot_id)]")
