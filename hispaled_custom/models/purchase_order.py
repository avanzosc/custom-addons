# -*- coding: utf-8 -*-
# Copyright 2019 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    delivery_partner_id = fields.Many2one(
        comodel_name='res.partner', string='Delivery address')
