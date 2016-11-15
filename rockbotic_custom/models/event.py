# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class EventTrack(models.Model):
    _inherit = 'event.track'

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Location',
        related='event_id.address_id', store=True, readonly=True)


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    address_id = fields.Many2one(
        comodel_name='res.partner', string='Address',
        related='event_id.address_id', store=True)
    organizer_id = fields.Many2one(
        string='Organizer', comodel_name='res.partner',
        related='event_id.organizer_id', store=True)
    parent_id = fields.Many2one(string='Parent', comodel_name='res.partner',
                                related='partner_id.parent_id', store=True)
    parent_name = fields.Char(related='parent_id.name')
    parent_mobile = fields.Char(related='parent_id.mobile')
    parent_email = fields.Char(related='parent_id.email')
