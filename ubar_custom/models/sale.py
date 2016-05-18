# -*- coding: utf-8 -*-
# (c) 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    standard_price = fields.Float('Cost Price',
                                  digits=dp.get_precision('Product Price'))
    move_ids = fields.One2many(
        comodel_name='stock.move', inverse_name='sale_line_id',
        string='Reservation', readonly=True, ondelete='set null')
    product_category = fields.Many2one(
        comodel_name='product.category', related='product_tmpl_id.categ_id',
        store=True)
    type_id = fields.Many2one(
        comodel_name='sale.order.type', related='order_id.type_id', store=True)

    @api.multi
    def product_id_change(self, pricelist, product, qty=0, uom=False,
                          qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False,
                          packaging=False, fiscal_position=False, flag=False):
        product_obj = self.env['product.product']
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty, uom, qty_uos, uos, name,
            partner_id, lang, update_tax, date_order, packaging,
            fiscal_position, flag)
        if product:
            product = product_obj.browse(product)
            res['value']['standard_price'] = product.standard_price
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    guarantee_limit = fields.Date(string='Warranty Expiration')
