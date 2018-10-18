# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_invoice_create(self, grouped=False, states=None,
                              date_invoice=False):
        invoice_id = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, states=states, date_invoice=date_invoice)
        invoice = self.env['account.invoice'].browse(invoice_id)
        invoice.sale_order_id = self.id
        return invoice_id


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False, warehouse_id=False):
        result = super(SaleOrderLine, self).product_id_change_with_wh(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag,
            warehouse_id=warehouse_id)
        if product and result.get('value', False):
            p = self.env['product.product'].browse(product)
            if p.variant_description:
                result['value']['name'] = p.variant_description
        return result
