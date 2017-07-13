# -*- coding: utf-8 -*-
# (c) 2017 Ainara Galdona - AvanzOSC
# (c) 2017 Gemma Bochaca i Royo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(
            self, pricelist, product_id, qty=0, uom=False, qty_uos=0,
            uos=False, name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product_id, qty=qty, uom=uom, qty_uos=qty_uos,
            uos=uos, name=name, partner_id=partner_id, lang=lang,
            update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if product_id:
            product = self.env['product.product'].browse(product_id)
            vals = product.get_partner_code_name(partner_id=partner_id)
            res['value']['name'] = u'[{}] {}'.format(vals.get('code', ''),
                                                     vals.get('name', ''))
            if product.description_sale:
                res['value']['name'] += '\n{}'.format(product.description_sale)
        return res
