# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAstikarCustom(common.TransactionCase):

    def setUp(self):
        super(TestAstikarCustom, self).setUp()
        self.ir_sequence_model = self.env['ir.sequence']
        self.mrp_repair_model = self.env['mrp.repair']
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

    def test_repair_action_done(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.assertEqual(self.mrp_repair.state, 'confirmed')
        self.mrp_repair.signal_workflow('repair_ready')
        self.assertEqual(self.mrp_repair.state, 'under_repair')
        self.assertEqual(self.mrp_repair.state, 'under_repair')
        self.mrp_repair.signal_workflow('action_repair_end')
        self.assertEqual(self.mrp_repair.state, 'not_invoice')
