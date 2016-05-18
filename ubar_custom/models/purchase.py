# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    carrier_id = fields.Many2one(
        comodel_name='delivery.carrier', string='Delivery method')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_category = fields.Many2one(
        comodel_name='product.category', related='product_id.categ_id',
        store=True)
