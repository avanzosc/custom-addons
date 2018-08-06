# -*- coding: utf-8 -*-
# Copyright © 2018 Mikel Urbistondo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizEventDeleteAssistant(models.TransientModel):
    _inherit = 'wiz.event.delete.assistant'

    reason_delete = fields.Selection(
        selection=[('m1', 'Does not have fun in class'),
                   ('m2', 'He does not like robotics'),
                   ('m3', 'Incompatibility of schedule'),
                   ('m4', 'High cost of activity'),
                   ('m5', 'Other motives'),
                   ('m6', 'Data/recording error')],
        string='Reason for the low')
    employee = fields.Many2one(
        string='Employee', comodel_name='hr.employee',
        related='registration.employee')

    @api.multi
    def action_delete(self):
        self.ensure_one()
        cond = [('event_id', 'in', self.env.context.get('active_ids')),
                ('partner_id', '=', self.partner.id),
                ('state', '=', 'open')]
        registrations = self.env['event.registration'].search(cond)\
            if not self.registration else self.registration
        result = super(WizEventDeleteAssistant, self).action_delete()
        registrations.write({'reason_delete': self.reason_delete})
        return result
