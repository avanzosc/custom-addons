# -*- coding: utf-8 -*-
# Copyright © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _


class WizSendEmailEventEvaluation(models.TransientModel):
    _name = 'wiz.send.email.event.evaluation'
    _description = 'Wizard for send evaluation email from event'

    body = fields.Html(string='Email body')

    @api.model
    def default_get(self, var_fields):
        res = super(WizSendEmailEventEvaluation, self).default_get(
            var_fields)
        template = self.env.ref(
            'rockbotic_custom.email_template_event_registration_evaluation',
            False)
        if not template:
            raise exceptions.Warning(
                _("Email template not found for event registration "
                  "evaluation"))
        res.update({'body': template.body_html})
        return res

    @api.multi
    def button_send_email(self):
        event_obj = self.env['event.event']
        for event in event_obj.browse(self.env.context.get('active_ids')):
            reg = event.no_employee_registration_ids
            reg._send_email_to_registrations_with_evaluation(self.body)
