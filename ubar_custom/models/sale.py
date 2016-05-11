# -*- coding: utf-8 -*-
# (c) 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    move_ids = fields.One2many(
        comodel_name='stock.move', inverse_name='sale_line_id',
        string='Reservation', readonly=True, ondelete='set null')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    guarantee_limit = fields.Date(string='Warranty Expiration')
