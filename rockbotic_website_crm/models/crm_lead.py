# -*- coding: utf-8 -*-
# Copyright © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    type = fields.Selection(selection_add=[('enroll', 'Enrollment')])
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain="[('is_group','=',True)]")
    event_id = fields.Many2one(
        comodel_name='event.event', string='Event',
        domain="[('address_id','=',school_id)]")
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
                'crm.action_crm_lead2opportunity_partner')
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
            account_type = self.env.ref('base_iban.bank_iban')
            vat = u'ES{}'.format(lead.vat) if lead.vat and\
                len(lead.vat) == 9 else lead.vat
            partner.write({
                'vat': vat,
                'bank_ids': [(0, 0, {
                    'state': account_type.code,
                    'acc_number': lead.account_number,
                    'mandate_ids': [(0, 0, {
                        'format': 'sepa',
                        'type': 'recurrent',
                        'recurrent_sequence_type': 'recurring',
                    })]
                })] if lead.account_number else [],
            })
            lead.parent_id = partner
        return partner_id

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
        self.write({'type': 'enroll'})
        return res