# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_claim_count(self):
        claim_obj = self.env['crm.claim']
        for partner in self:
            partner.claim_count = len(claim_obj.search(
                [('partner_id', 'child_of', partner.ids)]))

    magazine = fields.Boolean(string='Magazine', default=False)
    web_blog = fields.Boolean(string='Web/Blog', default=False)
    social_networks = fields.Boolean(string='Social networks', default=False)
    student_rockbotic_level = fields.Char(string='Rockbotic level')
    student_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Students',
        domain=[('active', '=', True), ('registered_partner', '=', True),
                ('employee_id', '=', False)])
    teacher_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Teachers',
        domain=[('active', '=', True), ('registered_partner', '=', True),
                ('employee_id', '!=', False)])
    other_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Contacts',
        domain=[('active', '=', True), ('registered_partner', '=', False)])
    claim_count = fields.Integer(compute='_compute_claim_count')
    send_email_unpaid_invoice = fields.Boolean(
        string='Send email unpaid invoice', default=False)
    accept_whatsapp = fields.Boolean(
        string='I accept and consent that my telephone number be used to send '
        'me communications whatsapp', default=False)
    accept_center_information = fields.Boolean(
        string='I accept and consent to send information from the center, for '
        'the purpose of commercial prospecting', default=False)

    @api.multi
    def show_crm_claims_from_partner(self):
        claim_obj = self.env['crm.claim']
        claims = claim_obj.search([('partner_id', 'child_of', self.ids)])
        res = {'view_mode': 'tree,form',
               'res_model': 'crm.claim',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'domain': [('id', 'in', claims.ids)]}
        return res
