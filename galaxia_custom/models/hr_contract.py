# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    communication_seg_soc_code = fields.Char('Seg. Soc. communication code')
    communication_contract_code = fields.Char('Contract communication code')


class HrContractHistorical(models.Model):
    _inherit = 'hr.contract.historical'

    @api.depends('hours')
    def _calculate_hours_percentage(self):
        for history in self:
            history.percentage = 0
            if history.hours > 0:
                history.percentage = (history.hours * 100) / 35

    hours = fields.Float(string='Hours')
    percentage = fields.Float(
        string='Percentage', digits=(2, 2), store=True,
        compute='_calculate_hours_percentage')
