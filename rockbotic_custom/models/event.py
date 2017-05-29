# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, exceptions, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    sale_order_payer = fields.Selection(
        related='sale_order.payer', string='Event payer',
        store=True)

    def _validate_registrations_email(self):
        for event in self:
            registrations = event.mapped(
                'no_employee_registration_ids').filtered(
                lambda x: not x.partner_id.parent_id.email)
            for registration in registrations:
                raise exceptions.Warning(_("Partner %s without email.") %
                                         registration.partner_id.name)

    def _send_email_to_registrations(self, body):
        template = self.env.ref(
            'event_registration_mass_mailing.email_template_event_'
            'registration', False)
        if not template:
            raise exceptions.Warning(
                _("Email template not found for event registration"))
        for event in self:
            for registration in event.no_employee_registration_ids:
                wizard = self.env['mail.compose.message'].with_context(
                    default_composition_mode='mass_mail',
                    default_template_id=template.id,
                    default_use_template=True,
                    active_id=registration.id,
                    active_ids=registration.ids,
                    active_model='event.registration',
                    default_model='event.registration',
                    default_res_id=registration.id,
                    force_send=True
                ).create({'body': body})
                wizard.send_mail()


class EventTrack(models.Model):
    _inherit = 'event.track'

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Location',
        related='event_id.address_id', store=True, readonly=True)


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Address',
        related='event_id.address_id', store=True)
    organizer_id = fields.Many2one(
        string='Organizer', comodel_name='res.partner',
        related='event_id.organizer_id', store=True)
    parent_id = fields.Many2one(string='Parent', comodel_name='res.partner',
                                related='partner_id.parent_id', store=True)
    parent_name = fields.Char(related='parent_id.name')
    parent_mobile = fields.Char(related='parent_id.mobile')
    parent_email = fields.Char(related='parent_id.email')
