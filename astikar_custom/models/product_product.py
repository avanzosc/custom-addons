# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields
from openerp.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _compute_sales_count(self):
        for product in self:
            product.repair_line_count = len(product.repair_line_ids)

    repair_line_ids = fields.One2many(
        comodel_name='mrp.repair.line', inverse_name='product_id',
        string='Repair line', domain=[('type', '=', 'add')])
    repair_line_count = fields.Integer(compute='_compute_sales_count')
    purchase_line_ids = fields.One2many(
        comodel_name='purchase.order.line', inverse_name='product_id',
        string='Purchase Lines')
    last_purchase_price = fields.Float(
        compute='_get_last_purchase', inverse='_inverse_last_purchase',
        store=True, digits=dp.get_precision('Product Price'))
    last_purchase_date = fields.Date(
        compute='_get_last_purchase', inverse='_inverse_last_purchase',
        store=True)
    last_supplier_id = fields.Many2one(
        compute='_get_last_purchase', inverse='_inverse_last_purchase',
        store=True)
    manual_purchase_price = fields.Float(
        string='Manual Last Purchase Price',
        digits=dp.get_precision('Product Price'))
    manual_purchase_date = fields.Date(string='Manual Last Purchase Date')
    manual_supplier_id = fields.Many2one(
        comodel_name='res.partner', string='Manual Last Supplier')

    @api.depends('purchase_line_ids.product_id', 'purchase_line_ids.state',
                 'purchase_line_ids.price_unit',
                 'purchase_line_ids.order_id.date_order',
                 'purchase_line_ids.order_id.partner_id')
    def _get_last_purchase(self):
        for record in self.filtered('purchase_line_ids'):
            if any(record.mapped('purchase_line_ids').filtered(
                    lambda l: l.state in ('done', 'confirmed'))):
                super(ProductProduct, record)._get_last_purchase()
            else:
                record.last_purchase_price = record.manual_purchase_price
                record.last_purchase_date = record.manual_purchase_date
                record.last_supplier_id = record.manual_supplier_id

    @api.multi
    def _inverse_last_purchase(self):
        """ set last purchase price, last purchase date and last supplier """
        for product in self:
            product.manual_purchase_price = product.last_purchase_price
            product.manual_purchase_date = product.last_purchase_date
            product.manual_supplier_id = product.last_supplier_id
