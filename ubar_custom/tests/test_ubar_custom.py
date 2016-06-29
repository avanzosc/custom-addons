# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestUbarCustom(common.TransactionCase):

    def setUp(self):
        super(TestUbarCustom, self).setUp()
        self.product_model = self.env['product.product']
        self.product = self.product_model.create({
            'name': 'Product Test',
            'uom_id': self.ref('product.product_uom_unit'),
            'default_code': 'A1PT',
            'old_reference': 'LA001',
            })
        self.analytic = self.env.ref('account.analytic_consultancy')
        self.quant_model = self.env['stock.quant']

    def test_name_search(self):
        product_ids = self.product_model.name_search(name='LA001', args=None)
        self.assertIn(self.product.id, ([a[0] for a in product_ids]),
                      'There is not any product with this old reference')
        product_ids = self.product_model.name_search('', args=None)
        all_product_ids = self.product_model.search('')
        self.assertEqual(len(product_ids), len(all_product_ids),
                         'Not the same quantity of products')

    def test_old_reference_change(self):
        message_count = len(self.product.message_ids)
        self.assertEquals(len(self.product.message_ids), message_count,
                          "There must not have been created a new message.")
        self.product.old_reference = 'LA002'
        message_ids = self.env['mail.message'].search([
            ('res_id', '=', self.product.id),
            ('model', '=', 'product.product')])
        self.assertEquals(len(message_ids), message_count + 1,
                          "There must have been created a new message.")

    def test_product_id_change(self):
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uos_qty': 7,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price,
            'project_by_task': 'no',
            'product_category': 1,
            'payer': 'student'}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.env['sale.order'].create(sale_vals)
        line = self.sale_order.order_line[0]
        res = self.env['sale.order.line'].product_id_change(
            self.sale_order.pricelist_id.id, line.product_id.id,
            qty=line.product_uom_qty, qty_uos=line. product_uos_qty,
            name=line.name, partner_id=self.sale_order.partner_id.id,
            update_tax=True, date_order=self.sale_order.date_order,
            fiscal_position=self.sale_order.fiscal_position.id)
        self.assertEqual(
            self.product.standard_price, res['value'].get('standard_price', 0),
            'Different standard price')

    def test_select_procurements(self):
        self.product.select_procurements()
        routes = self.env['stock.location.route'].search(
            ['&', ('product_selectable', '=', True),
             ('id', '!=', self.env.ref('mrp.route_warehouse0_manufacture').id)
             ])
        self.assertEqual(len(routes), len(self.product.route_ids))

    def test_compute_to_invoice(self):
        self.analytic.lot_id = self.ref('stock.lot_icecream_0')
        quant = self.quant_model.create({
            'lot_id': self.ref('stock.lot_icecream_0'),
            'qty': 1.0,
            'location_id': self.ref('stock.stock_location_stock'),
            'product_id': self.ref('stock.product_icecream'),
            })
        self.analytic.quant_id = quant
        self.assertEqual(self.analytic.remaining_ca, quant.to_invoice)
