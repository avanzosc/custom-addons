# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    communication_seg_soc_code = fields.Char('Seg. Soc. communication code')
    communication_contract_code = fields.Char('Contract communication code')
