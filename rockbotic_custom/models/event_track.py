# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Location',
        related='event_id.address_id', store=True, readonly=True)
