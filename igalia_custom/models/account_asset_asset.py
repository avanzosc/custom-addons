# -*- coding: utf-8 -*-
# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    @api.multi
    def compute_amortized_amount(self):
        for asset in self:
            lines = asset.mapped('depreciation_line_ids').filtered(
                lambda l: l.move_check)
            if lines:
                asset.amortized_amount = sum(lines.mapped('amount'))

    amortized_amount = fields.Float(
        string='Amortized amount', compute='compute_amortized_amount',
        digits_compute=dp.get_precision('Account'))
