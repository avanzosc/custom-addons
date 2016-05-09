# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, models, fields


class MakeCall(models.TransientModel):
    _name = 'make.call'

    @api.multi
    def create_call(self):
        call = self.env['crm.phonecall'].create({})
        call.make_call()
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.phonecall',
            'view_id': self.env.ref('crm.crm_case_phone_form_view').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': call[0].id,
            'context': self.env.context
        }
        return view
