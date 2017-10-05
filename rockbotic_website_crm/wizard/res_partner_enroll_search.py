# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, fields, models
from openerp.tools.safe_eval import safe_eval
from openerp.addons.base_iban.base_iban import _format_iban, _pretty_iban


class ResPartnerEnrollSearch(models.TransientModel):
    _name = 'res.partner.enroll.search'

    rockbotic_before = fields.Boolean()
    item_ids = fields.One2many(
        comodel_name='res.partner.enroll.search.item',
        inverse_name='search_id')
    partner_id = fields.Many2one(
        comodel_name='res.partner', domain="[('is_company','=',False)]")
    parent_id = fields.Many2one(
        comodel_name='res.partner', domain="[('is_company','=',True)]")

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(ResPartnerEnrollSearch, self).default_get(fields_list)
        if context.get('active_id'):
            lead = self.env['crm.lead'].browse(context['active_id'])
            res.update({
                'rockbotic_before': lead.rockbotic_before,
                'parent_id': lead.parent_id.id,
                'partner_id': lead.partner_id.id,
            })
            partner_obj = self.env['res.partner']
            partners = partner_obj.search(
                [('name', 'ilike', lead.contact_name),
                 ('parent_id', '!=', False),
                 ('registered_partner', '=', 'True'),
                 ('delete_after_sending_email', '=', False)])
            parents = partner_obj.search(
                [('is_company', '=', True),
                 ('delete_after_sending_email', '=', False),
                 '|', '|', '|', '|', ('name', 'ilike', lead.partner_name),
                 ('vat', 'ilike', lead.vat),
                 ('email', 'ilike', lead.email_from),
                 ('phone', 'ilike', lead.phone),
                 ('mobile', 'ilike', lead.phone)])
            partners |= partner_obj.search(
                [('parent_id', 'in', parents.ids),
                 ('delete_after_sending_email', '=', False),
                 ('registered_partner', '=', 'True')])
            if not partners:
                contact_names = lead.contact_name.split(' ')
                for contact_name in contact_names:
                    partners |= partner_obj.search(
                        [('name', 'ilike', contact_name),
                         ('delete_after_sending_email', '=', False),
                         ('registered_partner', '=', 'True'),
                         ('parent_id', '!=', False)]) if contact_name else\
                        partner_obj
                parent_names = lead.partner_name.split(' ')
                for parent_name in parent_names:
                    parents = partner_obj.search(
                        [('is_company', '=', True),
                         ('delete_after_sending_email', '=', False),
                         ('name', 'ilike', parent_name),
                         ('parent_id', '=', False)]) if parent_name else\
                        partner_obj
                partners |= partner_obj.search(
                    [('parent_id', 'in', parents.ids),
                     ('delete_after_sending_email', '=', False),
                     ('registered_partner', '=', 'True')])
            if partners:
                res.update({
                    'item_ids':
                        [(0, 0,
                          {'partner_id': x.id,
                           'parent_partner_id': x.parent_id.id,
                           'parent_acc_number':
                           x.parent_id.bank_ids.filtered(
                               lambda b: b.mandate_ids.filtered(
                                   lambda m: m.state == 'valid')
                           )[:1].acc_number or _('Valid mandate not found'),
                           'parent_vat': x.parent_id.vat}) for x
                         in partners],
                })
        return res

    @api.constrains('item_ids', 'rockbotic_before')
    def _check_selected_item_ids(self):
        for record in self.filtered('rockbotic_before'):
            selected_items = record.item_ids.filtered('checked')
            if not selected_items:
                raise exceptions.ValidationError(
                    _('Please select one line.'))
            elif len(selected_items) > 1:
                raise exceptions.ValidationError(
                    _('There can only be one selected.'))

    @api.multi
    def action_apply_same_parent(self):
        if self.rockbotic_before:
            item = self.item_ids.filtered('checked')[:1]
            self.parent_id = item.parent_partner_id
        return self.action_apply()

    @api.multi
    def action_apply(self):
        context = self.env.context
        lead = self.env[context.get('active_model')].browse(context.get(
            'active_id'))
        if self.rockbotic_before:
            item = self.item_ids.filtered('checked')[:1]
            partner = item.partner_id if not self.partner_id else \
                self.partner_id
            parent_id = lead._lead_create_contact(
                lead, lead.partner_name, True) if \
                not self.parent_id else self.parent_id.id
        else:
            parent_id = lead._lead_create_contact(
                lead, lead.partner_name, True) if \
                not self.parent_id else self.parent_id.id
            partner_id = lead._lead_create_contact(
                lead, lead.contact_name, False, parent_id=parent_id) if not \
                self.partner_id else self.partner_id.id
            partner = self.env['res.partner'].browse(partner_id)
        change_parent = partner.parent_id.id != parent_id
        if change_parent:
            change_wiz = self.env['res.partner.parent.change'].create({
                'partner_id': partner.id,
                'old_parent_id': partner.parent_id.id,
                'new_parent_id': parent_id,
            })
            change_wiz.change_parent_id()
        lead.write({
            'partner_id': partner.id,
            'parent_id': parent_id,
        })
        if not change_parent and lead.rockbotic_before and lead.account_number:
            acc_number = _pretty_iban(_format_iban(lead.account_number))
            bank = lead.parent_id.bank_ids.filtered(
                lambda b: b.acc_number == acc_number)
            mandates = lead.parent_id.mapped('bank_ids.mandate_ids')
            if not bank:
                account_type = self.env.ref('base_iban.bank_iban')
                mandates.filtered(
                    lambda m: m.state in ('draft', 'valid')).cancel()
                lead.parent_id.write({
                    'bank_ids': [(0, 0, {
                        'state': account_type.code,
                        'acc_number': acc_number,
                        'mandate_ids': [(0, 0, {
                            'format': 'sepa',
                            'type': 'recurrent',
                            'recurrent_sequence_type': 'recurring',
                        })],
                    })],
                })
            else:
                mandates.filtered(
                    lambda m: m.state in ('draft', 'valid') and
                    m.partner_bank_id != bank).cancel()
                if not bank.mandate_ids.filtered(
                        lambda m: m.state in ('draft', 'valid')):
                    bank.write({
                        'mandate_ids': [(0, 0, {
                            'format': 'sepa',
                            'type': 'recurrent',
                            'recurrent_sequence_type': 'recurring',
                        })],
                    })
        action = self.env.ref(
            'rockbotic_website_crm.action_crm_lead2opportunity_partner')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'active_id': context.get('active_id'),
            'active_ids': context.get('active_ids'),
            'active_model': context.get('active_model'),
        })
        return action_dict


class ResPartnerEnrollSearchItem(models.TransientModel):
    _name = 'res.partner.enroll.search.item'

    search_id = fields.Many2one(comodel_name='res.partner.enroll.search')
    checked = fields.Boolean(string='Selected')
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', readonly=True)
    parent_partner_id = fields.Many2one(
        comodel_name='res.partner', string='Parent', readonly=True)
    parent_vat = fields.Char(
        string='Parent VAT', readonly=True)
    parent_acc_number = fields.Char(string='Account Number', readonly=True)
