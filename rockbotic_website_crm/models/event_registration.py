# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons.event_track_assistant._common import\
    _convert_to_local_date


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.multi
    def _compute_first_day_of_class(self):
        for reg in self.filtered(
                lambda x: x.event_id and x.event_id.track_ids):
            session = min(reg.event_id.track_ids, key=lambda x: x.date)
            if session:
                reg.first_day_of_class = _convert_to_local_date(
                    session.date, self.env.user.tz)

    first_day_of_class = fields.Datetime(
        string='First day of class', compute='_compute_first_day_of_class')
