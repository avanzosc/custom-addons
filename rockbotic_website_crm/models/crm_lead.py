# -*- coding: utf-8 -*-
# Copyright © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _order = "create_date desc, priority desc, date_action, id desc"

    type = fields.Selection(selection_add=[('enroll', 'Enrollment')])
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain="[('is_group','=',True),('prospect', '=', False),"
               "('customer', '=', True),('payer', '=', 'student')]")
    event_id = fields.Many2one(
        comodel_name='event.event', string='Event',
        domain="[('address_id','=',school_id),"
               "('state','not in',('done','cancel'))]")
    account_type = fields.Many2one(comodel_name='res.partner.bank.type')
    account_number = fields.Char(string='Account Number')
    birth_date = fields.Date(string='Birthdate')
    course = fields.Char(string='Course')
    rockbotic_before = fields.Boolean(string='Rockbotic before')
    vat = fields.Char(string='Vat Number')
    journal_permission = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')], string='Journal')
    blog_permission = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')], string='Blog')
    media_permission = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')], string='Social Media')
    parent_id = fields.Many2one(
        comodel_name='res.partner', string='Parent',
        domain="[('is_company', '=', True)]")
    no_confirm_mail = fields.Boolean(string='Do Not Send Confirmation Mail')

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(CrmLead, self).default_get(fields_list) or {}
        if context.get('default_type') == 'enroll':
            res.update({
                'medium_id': self.env.ref(
                    'rockbotic_website_crm.crm_medium_student_signup').id,
            })
        return res

    @api.multi
    def button_convert2opportunity(self):
        self.ensure_one()
        signup = self.env.ref(
            'rockbotic_website_crm.crm_medium_student_signup')
        if self.medium_id == signup and not self.event_id:
            raise exceptions.Warning(_('Event must have been selected.'))
        action = self.env.ref(
            'rockbotic_website_crm.res_partner_enroll_search_action')
        if self.partner_id and self.parent_id and \
                self.partner_id.parent_id == self.parent_id or not \
                self.medium_id == signup:
            action = self.env.ref(
                'rockbotic_website_crm.action_crm_lead2opportunity_partner')
        action_dict = action.read()[0] if action else {}
        return action_dict

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id=parent_id)
        partner_obj = self.env['res.partner']
        partner = partner_obj.browse(partner_id)
        if parent_id:
            partner.write({
                'birthdate_date': lead.birth_date,
                'student_class': lead.course,
                'magazine': lead.journal_permission == 'yes',
                'web_blog': lead.blog_permission == 'yes',
                'social_networks': lead.media_permission == 'yes',
            })
        else:
            vat = u'ES{}'.format(lead.vat) if lead.vat and\
                len(lead.vat) == 9 else lead.vat
            country = (
                lead.country_id or self.env.user.company_id.country_id)
            bank_data = self._get_bank_data(lead.account_number, country)
            partner.write({
                'vat': vat,
                'bank_ids': [(0, 0, bank_data)] if bank_data else [],
            })
            lead.parent_id = partner
        return partner_id

    @api.model
    def _get_bank_data(self, account_number, country):
        if not account_number:
            return {}
        bank_obj = self.env['res.partner.bank']
        account_type = self.env.ref('base_iban.bank_iban')
        bank_data = {
            'state': account_type.code,
            'acc_number': account_number,
            'acc_country_id': country.id,
            'mandate_ids': [(0, 0, {
                'format': 'sepa',
                'type': 'recurrent',
                'recurrent_sequence_type': 'recurring',
            })],
        }
        if country:
            data = bank_obj.onchange_banco(
                account_number, country.id, account_type.code)
            bank_data.update(data.get('value', {}))
        if bank_data.get('bank'):
            data = bank_obj.onchange_bank_id(bank_data.get('bank'))
            bank_data.update(data.get('value', {}))
        return bank_data

    @api.model
    def _get_duplicated_leads_by_emails(
            self, partner_id, email, include_lost=False):
        lead_ids = super(CrmLead, self)._get_duplicated_leads_by_emails(
            partner_id, email, include_lost=include_lost)
        signup = self.env.ref(
            'rockbotic_website_crm.crm_medium_student_signup')
        leads = self.browse(lead_ids).filtered(
            lambda l: l.medium_id != signup and not l.event_registration_id)
        return leads.ids

    @api.multi
    def action_generate_event_registration(self, event):
        res = super(CrmLead, self).action_generate_event_registration(event)
        self.write({
            'type': 'enroll',
            'stage_id':
            self.env.ref('rockbotic_website_crm.crm_stage_enrolled').id,
        })
        self._send_email_registration_from_inscription()
        self._send_email_registration_sepa_from_inscription()
        return res

    def _send_email_registration_from_inscription(self):
        template = self.env.ref(
            'rockbotic_website_crm.email_to_new_registration_from_enrollment',
            False)
        if not template:
            raise exceptions.Warning(
                _("Email template not found for Confirmation of place from "
                  "inscription"))
        for lead in self.filtered(
                lambda x: x.event_registration_id and x.type == 'enroll'):
            vals = {'email_from': template.email_from,
                    'subject': template.subject,
                    'reply_to': template.reply_to,
                    'body': template.body_html}
            if self.partner_id.email:
                vals['partner_ids'] = [(6, 0, [self.partner_id.id])]
            if self.partner_id.parent_id and self.partner_id.parent_id.email:
                vals['partner_ids'] = [(6, 0, [self.partner_id.parent_id.id])]
            wizard = self.env['mail.compose.message'].with_context(
                default_composition_mode='mass_mail',
                default_template_id=template.id,
                default_use_template=True,
                default_no_auto_thread=True,
                active_domain=[['id', '=', lead.event_registration_id.id]],
                active_id=lead.event_registration_id.id,
                active_ids=lead.event_registration_id.ids,
                active_model='event.registration',
                default_model='event.registration',
                default_res_id=lead.event_registration_id.id,
            ).create(vals)
            wizard.send_mail()

    def _send_email_registration_sepa_from_inscription(self):
        template = self.env.ref(
            'rockbotic_website_crm.email_sepa_to_new_registration_from_'
            'enrollment', False)
        if not template:
            raise exceptions.Warning(
                _("Email template not found for request SEPA to the new "
                  "registration from inscription"))
        for lead in self.filtered(
            lambda x: x.event_registration_id and
            x.partner_id.parent_id.bank_ids and x.type == 'enroll' and
            x.partner_id.parent_id.bank_ids[0].mandate_ids and
            x.partner_id.parent_id.bank_ids[0].mandate_ids[0].state in (
                'draft', 'valid')):
            vals = {'email_from': template.email_from,
                    'subject': template.subject,
                    'reply_to': template.reply_to,
                    'body': template.body_html,
                    'partner_ids': [(6, 0, [self.partner_id.parent_id.id])]}
            mandate = lead.parent_id.bank_ids[0].mandate_ids[0]
            wizard = self.env['mail.compose.message'].with_context(
                default_composition_mode='mass_mail',
                default_template_id=template.id,
                default_use_template=True,
                default_no_auto_thread=True,
                active_domain=[['id', '=', mandate.id]],
                active_id=mandate.id,
                active_ids=mandate.ids,
                active_model='account.banking.mandate',
                default_model='account.banking.mandate',
                default_res_id=mandate.id,
            ).create(vals)
            wizard.send_mail()
            if mandate.state == 'draft':
                if not mandate.signature_date:
                    mandate.signature_date = fields.Datetime.now()
                mandate.validate()

    @api.model
    def redirect_opportunity_view(self, opportunity_id):
        if self.browse(opportunity_id).type == 'enroll':
            return {'type': 'ir.actions.act_window_close'}
        return super(CrmLead, self).redirect_opportunity_view(opportunity_id)

    @api.model
    def _convert_opportunity_data(self, lead, customer, section_id=False):
        vals = super(CrmLead, self)._convert_opportunity_data(
            lead, customer, section_id=section_id)
        if lead.type == 'enroll':
            del vals['type']
        return vals

    @api.onchange('school_id')
    def _onchange_school_id(self):
        self.user_id = self.school_id.user_id if self.school_id.user_id else\
            self.user_id

    @api.multi
    def create_registrations(self):
        partner_obj = self.env['res.partner']
        for signup in self.filtered(
                lambda s: not s.rockbotic_before and s.vat and
                s.type == 'enroll' and not s.event_registration_id):
            vat = (
                u'ES{}'.format(signup.vat) if len(signup.vat) == 9 else
                signup.vat)
            signup.parent_id = partner_obj.search([('vat', '=', vat)], limit=1)
            if not signup.parent_id:
                signup._lead_create_contact(
                    signup, signup.partner_name, True, parent_id=False)
            signup.partner_id = signup._lead_create_contact(
                signup, signup.contact_name, False,
                parent_id=signup.parent_id.id)
            if signup.partner_id and signup.parent_id:
                signup.action_generate_event_registration(signup.event_id)
        return True

    @api.model
    def create(self, values):
        lead = super(CrmLead, self).create(values)
        if (lead.type == 'enroll' and not lead.no_confirm_mail and
                lead.email_from):
            template = self.env.ref(
                'rockbotic_website_crm.email_to_new_enrollment', False)
            if not template:
                raise exceptions.Warning(
                    _("Email template not found for confirmation of "
                      "reservation of place"))
            lead.with_context(
                default_type='contact')._send_email_to_new_enrollment(
                template)
        return lead

    def _send_email_to_new_enrollment(self, template):
        partner_obj = self.env['res.partner']
        vals = {'email_from': template.email_from,
                'email_to': self.email_from,
                'subject': template.subject,
                'reply_to': template.reply_to,
                'body': template.body_html}
        wizard = self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_template_id=template.id,
            default_use_template=True,
            default_no_auto_thread=True,
            active_id=self.id,
            active_ids=self.ids,
            active_model='crm.lead',
            default_model='crm.lead',
            default_res_id=self.id,
        ).create(vals)
        wizard.send_mail()
        if (self.type == 'enroll' and not self.no_confirm_mail and
                self.email_from):
            cond = [('name', '=', self.email_from),
                    ('display_name', '=', self.email_from),
                    ('email', '=', self.email_from),
                    ('type', '=', 'contact')]
            partner = partner_obj.search(cond, limit=1)
            if partner:
                partner.delete_after_sending_email = True
