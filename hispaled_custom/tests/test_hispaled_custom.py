# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestHispaledCustom(common.TransactionCase):

    def setUp(self):
        super(TestHispaledCustom, self).setUp()
        self.tmpl_model = self.env['product.template'].with_context(
            check_variant_creation=True)
        self.attribute = self.env['product.attribute'].create({
            'name': 'Test Attribute',
            'attribute_code': 'TESTATTRIBUTE'
        })
        self.value1 = self.env['product.attribute.value'].create({
            'name': 'Value 1',
            'attribute_id': self.attribute.id,
        })
        self.value2 = self.env['product.attribute.value'].create({
            'name': 'Value 2',
            'attribute_id': self.attribute.id,
        })
        self.tmpl = self.tmpl_model.create({
            'name': 'Product Test Variant Description in lines',
            'no_create_variants': 'no',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})]})
        self.product = self.tmpl.product_variant_ids[:1]
        self.product.write({
            'name': 'Product Test Variant Description in lines',
            'description_sale': 'Product sale description',
            'variant_description': 'Product Variant Description in lines'})
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
        self.out_picking = self.browse_ref('stock.outgoing_chicago_warehouse')
        self.in_picking = self.browse_ref('stock.incomming_chicago_warehouse')
        self.group = self.browse_ref(
            'product_variants_no_automatic_creation.group_product_variant_'
            'extended_description')

    def test_variant_description_in_lines(self):
        res = self.po_line_model.onchange_product_id(
            self.pricelist, self.product.id, 5, self.product.uom_id.id,
            partner_id=self.partner)
        self.assertIn('Product Test Variant Description in lines',
                      res.get('value').get('name'))
        self.group.users = [(6, 0, self.env.user.ids)]
        res = self.po_line_model.onchange_product_id(
            self.pricelist, self.product.id, 5, self.product.uom_id.id,
            partner_id=self.partner)
        self.assertIn('Product Test Variant Description in lines',
                      res.get('value').get('name'))
        res = self.so_line_model.product_id_change_with_wh(
            self.pricelist, self.product.id, partner_id=self.partner)
        self.assertIn(self.product.name, res.get('value').get('name'))
        self.assertIn(
            self.product.description_sale, res.get('value').get('name'))
        res = self.move_model.with_context(
            default_picking_id=self.out_picking.id).onchange_product_id(
            self.product.id)
        self.assertIn(self.product.name, res.get('value').get('name'))
        self.assertIn(
            self.product.description_sale, res.get('value').get('name'))
        res = self.move_model.with_context(
            default_picking_id=self.in_picking.id).onchange_product_id(
            self.product.id)
        self.assertIn(self.product.name, res.get('value').get('name'))
        self.assertIn(
            self.product.variant_description, res.get('value').get('name'))
        res = self.invoice_line_model.with_context(
            type='out_invoice').product_id_change(
            self.product.id, self.product.uom_id.id,
            company_id=self.product.company_id.id, partner_id=self.partner)
        self.assertIn(self.product.name, res.get('value').get('name'))
        self.assertIn(
            self.product.description_sale, res.get('value').get('name'))
        res = self.invoice_line_model.with_context(
            type='in_invoice').product_id_change(
            self.product.id, self.product.uom_id.id,
            company_id=self.product.company_id.id, partner_id=self.partner)
        self.assertIn(self.product.name, res.get('value').get('name'))
        self.assertIn(
            self.product.variant_description, res.get('value').get('name'))

    def test_sale_info_in_invoices(self):
        invoice = self.invoice_model.browse(self.sale.action_invoice_create())
        self.assertEqual(invoice.sale_order_id.id, self.sale.id)
        wiz = self.wiz_payment_model.create({})
        wiz.with_context(active_ids=self.sale2.ids).create_invoices()
        cond = [('sale_order_id', '=', self.sale2.id)]
        invoice2 = self.invoice_model.search(cond, limit=1)
        self.assertNotEqual(invoice2, False)
