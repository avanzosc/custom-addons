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
    def button_template_sale_description(self):
        if (not self.product_id and self.product_tmpl_id and
                self.product_tmpl_id.description_sale):
            self.name = u"{}\n{}".format(
                self.name, self.product_tmpl_id.description_sale)

    @api.multi
    def button_confirm(self):
        result = super(SaleOrderLine, self.with_context(
            with_sale_description=True)).button_confirm()
        return result

    @api.multi
    def write(self, values):
        if (self.env.context.get('with_sale_description', False) and
                values.get('product_id', False)):
            product = self.env['product.product'].browse(
                values.get('product_id'))
            if (product.description_sale and product.description_sale not in
                    self.name):
                values['name'] = u"{}\n{}".format(
                    self.name, product.description_sale)
        return super(SaleOrderLine, self).write(values)
