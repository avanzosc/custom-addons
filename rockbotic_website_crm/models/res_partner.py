# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons.website.models.website import slug


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delete_after_sending_email = fields.Boolean(
        string='Delete after sending email', default=False)
    signup_slug = fields.Char(compute='_compute_slug_partner')

    @api.depends('name', 'is_group', 'prospect', 'customer', 'payer')
    def _compute_slug_partner(self):
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url', default='http://madrid.rockbotic.com')
        for partner in self.filtered(
                lambda p: p.is_group and not p.prospect and p.customer and
                p.payer == 'student'):
            partner.signup_slug = (
                '{}/page/student_signup/{}'.format(base_url, slug(partner)))
