# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.model
    def create(self, vals):
        sale_obj = self.env['sale.order']
        if vals.get('sale_order', False):
            sale = sale_obj.browse(vals.get('sale_order'))
            vals['organizer_id'] = sale.partner_id.id
            vals['address_id'] = sale.partner_shipping_id.id
        event = super(EventEvent, self).create(vals)
        return event


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    ampa_partner = fields.Boolean(string='AMPA partner', default=False)
