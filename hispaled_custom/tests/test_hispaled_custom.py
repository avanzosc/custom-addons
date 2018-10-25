# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHispaledCustom(common.TransactionCase):

    def setUp(self):
        super(TestHispaledCustom, self).setUp()
        self.product_obj = self.env['product.product']
        self.po_line_model = self.env['purchase.order.line']
        self.so_line_model = self.env['sale.order.line']
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.move_model = self.env['stock.move']
        self.wiz_payment_model = self.env['sale.advance.payment.inv']
        self.pricelist = self.ref('product.list0')
        self.partner = self.ref('base.res_partner_1')
        self.fp = self.ref('account.fiscal_position_normal_taxes_template1')
        self.sale = self.browse_ref('sale.sale_order_1')
        self.sale2 = self.browse_ref('sale.sale_order_2')

    def test_variant_description_in_lines(self):
        product = self.product_obj.create({
            'name': 'Product Test Variant Description in lines',
            'variant_description': 'Product Variant Description in lines'})
        res = self.po_line_model.onchange_product_id(
            self.pricelist, product.id, 5, product.uom_id.id,
            partner_id=self.partner)
        self.assertEqual(
            res.get('value').get('name'), product.variant_description)
        res = self.so_line_model.product_id_change_with_wh(
            self.pricelist, product.id, partner_id=self.partner)
        self.assertEqual(
            res.get('value').get('name'), product.variant_description)
        res = self.move_model.onchange_product_id(product.id)
        self.assertEqual(
            res.get('value').get('name'), product.variant_description)
        res = self.invoice_line_model.product_id_change(
            product.id, product.uom_id.id, company_id=product.company_id.id,
            partner_id=self.partner)
        self.assertEqual(
            res.get('value').get('name'), product.variant_description)

    def test_sale_info_in_invoices(self):
        invoice = self.invoice_model.browse(self.sale.action_invoice_create())
        self.assertEqual(invoice.sale_order_id.id, self.sale.id)
        wiz = self.wiz_payment_model.create({})
        wiz.with_context(active_ids=self.sale2.ids).create_invoices()
        cond = [('sale_order_id', '=', self.sale2.id)]
        invoice2 = self.invoice_model.search(cond, limit=1)
        self.assertNotEqual(invoice2, False)
