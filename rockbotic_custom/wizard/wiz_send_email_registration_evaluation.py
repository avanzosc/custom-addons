# -*- coding: utf-8 -*-
# Copyright © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _


class WizSendEmailRegistrationEvaluation(models.TransientModel):
    _name = 'wiz.send.email.registration.evaluation'
    _description = 'Wizard for send email to registration evaluation'

    body = fields.Html(string='Email body')

    @api.model
    def default_get(self, var_fields):
        res = super(WizSendEmailRegistrationEvaluation, self).default_get(
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
        registration_obj = self.env['event.registration']
        registrations = registration_obj.browse(self.env.context.get(
            'active_ids')).filtered(lambda x: not x.employee)
        registrations._send_email_to_registrations_with_evaluation(self.body)
