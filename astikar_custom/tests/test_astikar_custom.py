# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestAstikarCustom(common.TransactionCase):

    def setUp(self):
        super(TestAstikarCustom, self).setUp()
        self.ir_sequence_model = self.env['ir.sequence']
        self.mrp_repair_model = self.env['mrp.repair']
        self.quant_model = self.env['stock.quant']
        self.mrp_repair_sequence = self.browse_ref('mrp_repair.seq_mrp_repair')
        self.product = self.browse_ref('product.product_product_3')
        self.location = self.ref('stock.location_inventory')
        self.mrp_repair1 = self.env.ref('mrp_repair.mrp_repair_rmrp1')
        self.mrp_repair = self.mrp_repair_model.create({
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'location_id': self.location,
            'location_dest_id': self.location,
            })

    def test_default_quotation_note(self):
        note = 'Test Sale Note'
        self.env.user.company_id.sale_note = note
        repair = self.mrp_repair_model.new(
            self.mrp_repair_model.default_get(['quotation_notes']))
        self.assertTrue(repair.quotation_notes)
        self.assertEqual(repair.quotation_notes,
                         self.env.user.company_id.sale_note)
        self.assertEqual(repair.quotation_notes,
                         note)

    def test_new_repair_sequence_assign(self):
        name = self._get_next_name()
        mrp_repair = self.mrp_repair_model.create({
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'location_id': self.location,
            'location_dest_id': self.location,
        })
        self.assertNotEqual(mrp_repair.name, '/')
        self.assertEqual(mrp_repair.name, name)

    def test_copy_repair_sequence_assign(self):
        name = self._get_next_name()
        mrp_repair_copy = self.mrp_repair.copy()
        self.assertNotEqual(mrp_repair_copy.name, self.mrp_repair.name)
        self.assertEqual(mrp_repair_copy.name, name)

    def _get_next_name(self):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(
            self.mrp_repair_sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(
            self.mrp_repair_sequence.suffix, d)
        name = (prefix + ('%%0%sd' % self.mrp_repair_sequence.padding %
                          self.mrp_repair_sequence.number_next_actual) +
                suffix)
        return name

    def test_shortcuts(self):
        res = self.mrp_repair.action_show_purchase_order()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window')
        res = self.mrp_repair.action_show_account_invoice()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window')
        res = self.mrp_repair.action_show_purchase_order_lines()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window')
        res = self.mrp_repair.action_show_account_invoice_lines()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window')

    def test_invoice_line_product_change(self):
        invoice_line = self.env.ref(
            'account.demo_invoice_0_line_rpanrearpanelshe0')
        inv = invoice_line.invoice_id
        res = invoice_line.product_id_change(
            invoice_line.product_id.id, invoice_line.uos_id.id,
            qty=invoice_line.quantity, name=invoice_line.name,
            type=inv.type, partner_id=inv.partner_id.id,
            fposition_id=inv.fiscal_position.id,
            price_unit=invoice_line.price_unit, currency_id=inv.currency_id.id,
            company_id=inv.company_id.id)
        if res.get('value', False) and 'account_analytic_id' in res['value']:
            self.assertNotEqual(
                res['value'].get('account_analytic_id', False), False)

    def test_repair_totals(self):
        product = self.env.ref('product.product_product_34')
        repair_line_vals = {
            'repair_id': self.mrp_repair.id,
            'product_id': product.id,
            'product_uom_qty': 0,
            'expected_qty': 2,
            'name': product.name,
            'product_uom': product.uom_id.id,
            'type': 'add',
            'location_id': self.location,
            'location_dest_id': product.property_stock_production.id,
            'price_unit': 2,
            'to_invoice': True}
        fee_line_vals = {
            'repair_id': self.mrp_repair.id,
            'product_id': product.id,
            'product_uom_qty': 3,
            'name': product.name,
            'product_uom': product.uom_id.id,
            'location_id': self.location,
            'location_dest_id': product.property_stock_production.id,
            'price_unit': 2,
            'to_invoice': True}
        repair_line = self.env['mrp.repair.line'].create(repair_line_vals)
        self.env['mrp.repair.fee'].create(fee_line_vals)
        self.assertEqual(self.mrp_repair.amnt_untaxed, 10,
                         "Untaxed amount not correct")
        self.assertEqual(self.mrp_repair.amnt_tax, 0,
                         "Taxed amount not correct")
        self.assertEqual(self.mrp_repair.amnt_total, 10,
                         "Total amount not correct")
        repair_line.product_uom_qty = 2
        self.assertEqual(repair_line.load_cost, True, "Load cost updated")

    def test_compute_repair_count(self):
        self.assertEqual(self.product.repair_line_count, 0)
        repair_line_vals = {
            'repair_id': self.mrp_repair.id,
            'product_id': self.product.id,
            'product_uom_qty': 0,
            'expected_qty': 2,
            'name': self.product.name,
            'product_uom': self.product.uom_id.id,
            'type': 'add',
            'location_id': self.location,
            'location_dest_id': self.product.property_stock_production.id,
            'price_unit': 2,
            'to_invoice': True}
        self.env['mrp.repair.line'].create(repair_line_vals)
        self.assertEqual(len(self.product.repair_line_ids), 1)
        repair_line_vals2 = {
            'repair_id': self.mrp_repair.id,
            'product_id': self.product.id,
            'product_uom_qty': 0,
            'expected_qty': 2,
            'name': self.product.name,
            'product_uom': self.product.uom_id.id,
            'type': 'remove',
            'location_id': self.location,
            'location_dest_id': self.product.property_stock_production.id,
            'price_unit': 2,
            'to_invoice': True}
        self.env['mrp.repair.line'].create(repair_line_vals2)
        self.assertEqual(len(self.product.repair_line_ids), 1)

    def test_compute_date_due(self):
        self.assertEqual(fields.Date.today(), self.mrp_repair.date_due)
        self.mrp_repair.partner_id = self.ref('base.res_partner_2')
        payment_term = self.mrp_repair.partner_id.property_payment_term
        payment_days = payment_term.line_ids[0].days
        date = fields.Date.from_string(fields.Date.today())
        self.assertEqual(
            fields.Date.to_string(date + relativedelta(days=payment_days)),
            self.mrp_repair.date_due)

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
            'price_unit': self.product.list_price}
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

    def test_create_invoice(self):
        self.mrp_repair1.partner_id.invoice_warn = 'warning'
        self.mrp_repair1.partner_id.invoice_warn_msg = 'Warning invoice'
        self.mrp_repair1.invoice_method = 'b4repair'
        self.mrp_repair1.signal_workflow('repair_confirm')
        self.mrp_repair1.action_invoice_create()
        self.assertFalse(self.mrp_repair1.invoice_id.not_warning)

    def test_quant_valuation(self):
        self.product.sudo().write({'cost_method': 'real',
                                   'standard_price': 20,
                                   'manual_standard_cost': 35})
        quant = self.quant_model.create(
            {'product_id': self.product.id,
             'cost': 20,
             'location_id': self.location,
             'qty': 5})
        self.assertEqual(quant.standard_value, (20 * 5),
                         "Incorrect Manual Value for quant.")

    def test_wizard_mrp_repair_fee(self):
        wiz = self.env['wiz.mrp.repair.fee'].create({
            'imputation_date': fields.Date.today(),
        })
        res = wiz.show_mrp_repair_fee()
        self.assertTrue(res['context']['default_is_from_menu'])
        self.assertTrue(res['context']['search_default_is_from_menu'])
