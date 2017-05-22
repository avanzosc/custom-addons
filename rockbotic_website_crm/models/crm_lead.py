# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain="[('is_group','=',True)]")
    event_id = fields.Many2one(comodel_name='event.event', string='Event')
    account_type = fields.Many2one(comodel_name='res.partner.bank.type')
    account_number = fields.Char(string='Account Number')
    birth_date = fields.Date(string='Birth date')
    course = fields.Char(string='Course')
    rockbotic_before = fields.Boolean(string='Rockbotic before')
    vat = fields.Char(string='Vat Number')

    @api.multi
    @api.onchange('school_id')
    def _onchange_school_id(self):
        for lead in self:
            if lead.school_id:
                return {'domain': {
                        'event_id': [('address_id', '=', lead.school_id.id),
                                     ('state', 'not in', ('done', 'cancel'))],
                        }}

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id=parent_id)
        partner_obj = self.env['res.partner']
        partner = partner_obj.browse(partner_id)
        data = {
            'birthdate_date': lead.birth_date,
            'student_class': lead.course,
        }
        print lead.account_type
        if parent_id:
            parent = partner_obj.browse(parent_id)
            data_parent = {
                'vat': lead.vat,
                'bank_ids': [(0, 0, {
                    'state': lead.account_type.code,
                    'acc_number': lead.account_number,
                    'mandate_ids': [(0, 0, {
                        'format': 'sepa',
                        'type': 'recurrent',
                        'recurrent_sequence_type': 'recurring',
                    })]
                })]
            }
            parent.write(data_parent)
        partner.write(data)
        return partner_id
