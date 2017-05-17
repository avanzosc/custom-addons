# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    key_code = fields.Char()


class EventTrackPresence(models.Model):
    _inherit = 'event.track.presence'

    @api.depends('session', 'session.allowed_partner_ids')
    def _compute_allowed_partner_ids(self):
        if self.env['marketing.config.settings']._get_parameter(
           'show.all.customers.in.presences'):
            cond = [('employee_id', '!=', False)]
            customers = self.env['res.partner'].search(cond)
        for presence in self:
            presence.allowed_partner_ids = (
                [(6, 0, presence.session.allowed_partner_ids.ids)])
            if self.env['marketing.config.settings']._get_parameter(
               'show.all.customers.in.presences'):
                for customer in customers:
                    presence.allowed_partner_ids = [(4, customer.id)]
