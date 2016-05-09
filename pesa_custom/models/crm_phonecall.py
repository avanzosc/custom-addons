# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, fields, models


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    @api.multi
    def hang_up_call(self):
        super(CrmPhonecall, self).hang_up_call()
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.phonecall',
            'view_id': self.env.ref('crm.crm_case_phone_form_view').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'readonly': True,
            'res_id': self.id,
            'context': self.env.context
        }
        return view