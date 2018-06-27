# -*- coding: utf-8 -*-
# (c) 2017 Ainara Galdona - AvanzOSC
# (c) 2017 Gemma Bochaca i Royo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product_id, qty=0, uom=False, qty_uos=0,
            uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False, warehouse_id=False):
        res = super(SaleOrderLine, self).product_id_change_with_wh(
            pricelist, product_id, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag,
            warehouse_id=warehouse_id)
        value = res.setdefault('value', {})
        if product_id:
            product = self.env['product.product'].browse(product_id)
            partner = self.env['res.partner'].browse(partner_id)
            partner_name = partner.parent_id or partner
            if partner.lang:
                self = self.with_context(lang=partner.lang)
            value['name'] = u'[{}] {}'.format(
                product.get_real_code(partner_id=partner_name),
                product.get_real_name(partner_id=partner_name))
            if product.description_sale:
                value['name'] += '\n' + product.description_sale
        return res
