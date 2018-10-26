# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons.website.models.website import slug


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delete_after_sending_email = fields.Boolean(
        string='Delete after sending email', default=False)
    signup_slug = fields.Char(compute='_compute_slug_partner', store=True)
    event_web_warning = fields.Boolean(string='Warn about event in website')

    @api.depends('name', 'is_group', 'prospect', 'customer', 'payer')
    def _compute_slug_partner(self):
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url', default='http://madrid.rockbotic.com')
        for partner in self.filtered(
                lambda p: p.is_group and not p.prospect and p.customer and
                p.payer == 'student'):
            try:
                partner_slug = slug(partner)
            except Exception:
                partner_slug = partner.id or ''
            partner.signup_slug = (
                '{}/page/student_signup/{}'.format(base_url, partner_slug))

    @api.multi
    def button_recompute_slug(self):
        fields_list = ['signup_slug']
        for field in fields_list:
            self.env.add_todo(self._fields[field], self)
        self.recompute()
