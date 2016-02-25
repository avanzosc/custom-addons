# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    key_code = fields.Char()
