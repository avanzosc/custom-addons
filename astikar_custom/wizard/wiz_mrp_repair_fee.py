# -*- coding: utf-8 -*-
# (c) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class WizMrpRepairFee(models.TransientModel):
    _inherit = 'wiz.mrp.repair.fee'

    @api.multi
    def show_mrp_repair_fee(self):
        res = super(WizMrpRepairFee, self).show_mrp_repair_fee()
        res['context'].update({'default_is_from_menu': True})
        return res
