# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    @api.multi
    def compute_depreciation_board(self):
        result = super(AccountAssetAsset, self).compute_depreciation_board()
        for asset in self.filtered(lambda x: x.method_time == 'number'):
            for line in asset.depreciation_line_ids:
                line.method_percentage = round(
                    ((line.amount * 100) / asset.purchase_value), 2)
            if asset.depreciation_line_ids:
                max_line = max(asset.depreciation_line_ids, key=lambda x: x.id)
                lines = asset.depreciation_line_ids.filtered(
                    lambda x: x.id != max_line.id)
                perc = sum(lines.mapped('method_percentage'))
                i = len(asset.depreciation_line_ids) - 1
                asset.depreciation_line_ids[i].method_percentage = 100 - perc
        return result
