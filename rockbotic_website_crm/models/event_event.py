# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons.website.models.website import slug


class EventEvent(models.Model):
    _inherit = 'event.event'

    signup_slug = fields.Char(compute='_compute_slug_event')

    @api.depends('name', 'address_id', 'address_id.signup_slug')
    def _compute_slug_event(self):
        for event in self.filtered(lambda e: e.address_id.signup_slug):
            try:
                event_slug = slug(event)
            except Exception:
                event_slug = event.id or ''
            event.signup_slug = (
                '{}/{}'.format(event.address_id.signup_slug, event_slug))
