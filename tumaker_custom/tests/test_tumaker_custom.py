# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields, exceptions


class TestTumakerCustom(common.TransactionCase):

    def setUp(self):
        super(TestTumakerCustom, self).setUp()
        self.crm_sale_wiz_obj = self.env['crm.make.sale']
        self.analytic_model = self.env['account.analytic.account']
        self.analytic_line_model = self.env['account.analytic.line']
        self.purchase_model = self.env['purchase.order']
        self.purchase_line_model = self.env['purchase.order.line']
        self.invoice_model = self.env['account.invoice']
        self.location_obj = self.env['stock.location']
        self.sale_model = self.env['sale.order']
        self.product_model = self.env['product.product']
        self.production_model = self.env['mrp.production']
        self.bom = self.env.ref('mrp.mrp_bom_1')
        self.partner_id = self.ref('base.res_partner_5')
        self.pricelist_id = self.ref('purchase.list0')
        self.picking = self.env.ref('stock.incomming_shipment')
        self.wiz_obj = self.env['stock.transfer_details']
        self.location = self.env['stock.location'].create(
            {'name': 'Test Location',
             'usage': 'internal'})
        analytic_vals = {
            'name': 'Analytic test',
            'type': 'normal',
            'quantity_max': 100,
            'partner_id': self.partner_id,
            'pricelist_id': self.pricelist_id,
            }
        self.analytic_id = self.analytic_model.create(analytic_vals)
        self.product_id = self.env.ref('product.product_product_6')
        self.acc = (self.product_id.property_account_expense.id or
                    self.product_id.categ_id.property_account_expense_categ.id)
        analytic_line_vals = {
            'account_id': self.analytic_id.id,
            'name': 'Test line',
            'general_account_id': self.acc,
            'journal_id': self.ref('hr_timesheet.analytic_journal'),
            'product_id': self.product_id.id,
            'amount': 25,
            'unit_amount': 10,
            'facturable_qty': 10,
            'to_invoice': self.ref(
                'hr_timesheet_invoice.timesheet_invoice_factor1')
            }
        self.analytic_line1 = self.analytic_line_model.create(
            analytic_line_vals)
        self.product_id2 = self.env.ref('product.product_product_12')
        analytic_line_vals['facturable_qty'] = 15
        analytic_line_vals['product_id'] = self.product_id2.id
        self.analytic_line2 = self.analytic_line_model.create(
            analytic_line_vals)
        purchase_vals = {
            'partner_id': self.partner_id,
            'pricelist_id': self.pricelist_id,
            'location_id': self.location_obj.search(
                [('usage', '=', 'internal')], limit=1).id
            }
        self.purchase_id = self.purchase_model.create(purchase_vals)
        self.stockable_product = self.env.ref('product.product_product_3')
        self.service_product = self.env.ref('product.product_product_2')
        self.service_product.auto_create_task = True
        self.project = self.env.ref('project.project_project_1')
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'project_id': self.project.id,
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': self.stockable_product.id,
            'name': self.stockable_product.name,
            'product_uos_qty': 7,
            'product_uom': self.stockable_product.uom_id.id,
            'price_unit': self.stockable_product.list_price}
        sale_line_vals2 = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uos_qty': 7,
            'product_uom': self.service_product.uom_id.id,
            'price_unit': self.service_product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals),
                                   (0, 0, sale_line_vals2)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.black_product = self.env.ref('product.product_product_4b')
        self.crm_lead = self.env.ref('crm.crm_case_1')
        self.warehouse = self.env['stock.warehouse'].create({'name': 'New WRH',
                                                             'code': 'NEW',
                                                             })

    def test_print_float_time_widget(self):
        text = self.analytic_id.convert_to_float_time_widget(20.5)
        self.assertEqual(text, '20:30')
        text = self.analytic_id.convert_to_float_time_widget(2.25)
        self.assertEqual(text, '02:15')

    def test_analytic_computed_vals(self):
        self.assertEqual(
            self.analytic_id.consumed_hours, 25,
            'Analytic invalid consumed hours')
        self.assertEqual(
            self.analytic_id.remaining_hours, 75,
            'Analytic invalid remaining hours')
        self.assertFalse(self.analytic_id.is_overdue_quantity)
        analytic_line_vals = {
            'account_id': self.analytic_id.id,
            'name': 'Test line',
            'general_account_id': self.acc,
            'journal_id': self.ref('hr_timesheet.analytic_journal'),
            'product_id': self.product_id.id,
            'amount': 25,
            'unit_amount': 10,
            'facturable_qty': 100,
            'to_invoice': self.ref(
                'hr_timesheet_invoice.timesheet_invoice_factor1')
            }
        self.analytic_line_model.create(analytic_line_vals)
        self.assertTrue(self.analytic_id.is_overdue_quantity)

    def test_analytic_line_prepare_invoice_line(self):
        invoices = self.analytic_id.line_ids.invoice_cost_create()
        for invoice in self.invoice_model.browse(invoices):
            lines = invoice.invoice_line.filtered(
                lambda x: x.product_id == self.product_id)
            self.assertEqual(lines.quantity, 10,
                             'Invoice line quantity is not correct')
            lines2 = invoice.invoice_line.filtered(
                lambda x: x.product_id == self.product_id2)
            self.assertEqual(lines2.quantity, 15,
                             'Invoice line quantity is not correct')

    def test_analytic_line_prepare_invoice_line_force_product(self):
        force_product = self.ref('product.product_product_1')
        data = {'product': force_product, 'date': fields.Date.today(),
                'time': True, 'name': 'Test Invoice'}
        invoices = self.analytic_id.line_ids.invoice_cost_create(data)
        for invoice in self.invoice_model.browse(invoices):
            lines = invoice.invoice_line.filtered(
                lambda x: x.product_id.id == force_product)
            self.assertNotEqual(len(lines), 0,
                                'Forced product line quantity is not correct')

    def test_analytic_line_prepare_invoice_line_no_acc(self):
        self.product_id.property_account_income = False
        self.product_id.categ_id.property_account_income_categ = False
        with self.assertRaises(exceptions.Warning):
            self.analytic_id.line_ids.invoice_cost_create()

    def test_purchase_line_onchange(self):
        self.product_id.expense_analytic_account_id = self.analytic_id.id
        purchase_line_vals = {
            'product_id': self.product_id.id,
            'order_id': self.purchase_id.id,
            'product_qty': 15,
            'price_unit': 20,
            'name': 'test purchase line',
            'date_planned': fields.Date.today()
            }
        self.purchase_line_model.create(purchase_line_vals)
        val = self.purchase_line_model.onchange_product_id(
            self.pricelist_id, self.product_id.id, 15,
            self.product_id.uom_po_id.id, self.partner_id)
        self.assertEqual(val['value'].get('account_analytic_id'),
                         self.analytic_id.id,
                         'Purchase line analytic account is not correct.')

    def test_sale_order(self):
        self.sale_order.action_wait()
        self.sale_order.action_ship_create()
        self.sale_order.procurement_group_id.procurement_ids.run()
        self.assertEqual(self.sale_order.shipped, False,
                         "Sale order is shipped, and it can't be.")
        self.assertEqual(self.sale_order.task_exists, True,
                         "Sale order tasks has not been created.")
        res = self.sale_order.action_view_task()
        self.assertEqual(res.get('type', False), 'ir.actions.act_window',
                         "Returned action is not correct")

    def test_project_childs(self):
        analytic_acc = self.project.analytic_account_id
        childs = self.env['project.project'].search(
            [('analytic_account_id', 'in', analytic_acc.child_ids.ids)])
        self.assertEqual(self.project.project_child_ids.ids, childs.ids,
                         "Project Child field is not correct")

    def test_do_detailed_transfer(self):
        self.picking.action_confirm()
        self.assertEqual(self.picking.state, 'assigned')
        for line in self.picking.move_lines:
            line.price_unit = 0
        self.picking.do_enter_transfer_details()
        wiz = self.wiz_obj.with_context({
            'active_id': self.picking.id,
            'active_ids': [self.picking.id],
            'active_model': 'stock.picking'
        }).create({'picking_id': self.picking.id})
        with self.assertRaises(exceptions.Warning):
            wiz.do_detailed_transfer()
        wiz.allow_zero_cost = True
        wiz.do_detailed_transfer()
        self.assertEqual(self.picking.state, 'done')

    def test_product_search_name(self):
        res = self.product_model.name_search('Black')
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id in searched_products),
                        "No black product searched")

    def test_product_search_name_negative(self):
        res = self.product_model.name_search('Black', operator="not like")
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id not in searched_products),
                        "Black product searched")

    def test_product_search_non_exists_product(self):
        res = self.product_model.name_search('NotExists')
        self.assertTrue((not res), 'Product searched')

    def test_product_search_pattern(self):
        self.black_product.default_code = 'COD25'
        res = self.product_model.name_search('COD25')
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id in searched_products),
                        "Black product searched")

    def test_product_ean_search(self):
        self.black_product.ean13 = '8431311550618'
        res = self.product_model.name_search('131155')
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id in searched_products),
                        "Black product searched")

    def test_product_search_suppinfo(self):
        suppinfo_model = self.env['product.supplierinfo']
        suppinfo_model.create({
            'product_tmpl_id': self.black_product.product_tmpl_id.id,
            'name': self.partner_id,
            'product_code': 'TestName',
            'type': 'customer'})
        suppinfo_model.create({
            'product_tmpl_id': self.black_product.product_tmpl_id.id,
            'name': self.partner_id,
            'product_code': 'CODXXTEST',
            'type': 'supplier'})
        res = self.product_model.name_search('TestName')
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id in searched_products),
                        "Black product searched")
        res = self.product_model.name_search('CODXXTEST')
        searched_products = [x[0] for x in res]
        self.assertTrue((self.black_product.id in searched_products),
                        "Black product searched")

    def test_default_sale_note(self):
        note = 'Test Sale Note'
        self.env.user.company_id.sale_note_report = note
        sale = self.sale_model.new(
            self.sale_model.default_get(['sale_note']))
        self.assertTrue(sale.sale_note)
        self.assertEqual(sale.sale_note,
                         self.env.user.company_id.sale_note_report)
        self.assertEqual(sale.sale_note, note)

    def test_do_detailed_transfer_more_qty(self):
        purchase_line_vals = {
            'product_id': self.product_id.id,
            'order_id': self.purchase_id.id,
            'product_qty': 15,
            'price_unit': 20,
            'name': 'test purchase line',
            'date_planned': fields.Date.today()
        }
        self.purchase_line_model.create(purchase_line_vals)
        self.purchase_id.signal_workflow('purchase_confirm')
        picking = self.purchase_id.mapped('order_line.move_ids.picking_id')[:1]
        self.assertEqual(picking.state, 'assigned')
        picking.do_enter_transfer_details()
        pre_line_count = len(picking.move_lines)
        for line in picking.move_lines:
            self.assertTrue(line.purchase_line_id)
        wiz = self.wiz_obj.with_context({
            'active_id': picking.id,
            'active_ids': [picking.id],
            'active_model': 'stock.picking'
        }).create({'picking_id': picking.id})
        wiz.item_ids[:1].quantity += 3
        wiz.do_detailed_transfer()
        post_line_count = len(picking.move_lines)
        self.assertNotEqual(pre_line_count, post_line_count)
        for line in picking.move_lines:
            self.assertTrue(line.purchase_line_id)

    def test_get_move_analysis_report(self):
        invoice = self.env.ref('account.invoice_1')
        invoice.journal_id.update_posted = True
        invoice.signal_workflow('invoice_cancel')
        invoice.action_cancel_draft()
        invoice.invoice_line.write({'product_id': self.product_id.id})
        invoice.signal_workflow('invoice_open')
        rep_model = self.env['account.entries.report']
        self.assertTrue(rep_model.search([('product_id', '!=', False)]))
        self.assertFalse(rep_model.search(
            [('product_id', '!=', False), ('product_categ_id', '=', False)]))

    def test_move_compute_subtotal(self):
        for move in self.picking.move_lines:
            subtotal = (
                move.purchase_line_id.price_unit * move.product_uom_qty *
                (1 - (move.purchase_line_id.discount / 100)))
            self.assertEqual(move.price_subtotal, subtotal)

    def test_production_change(self):
        production = self.production_model.create(
            {'product_id': self.bom.product_tmpl_id.id,
             'product_qty': 100,
             'product_uom': self.bom.product_tmpl_id.uom_id.id,
             'bom_id': self.bom.id,
             })
        self.assertNotEqual(production.location_src_id, self.location)
        self.bom.routing_id.location_id = self.location
        production.routing_id = self.bom.routing_id
        production.onchange_routing_id()
        self.assertEqual(production.location_src_id, self.location)

    def test_crm_lead_make_sale(self):
        self.crm_lead.partner_id = self.partner_id
        crm_sale_wiz = self.crm_sale_wiz_obj.with_context(
            active_id=self.crm_lead.id, active_ids=[self.crm_lead.id],
            active_model='crm.lead').create({
                'warehouse_id': self.warehouse.id})
        action = crm_sale_wiz.makeOrder()
        sale_id = action.get('res_id')
        sale = self.sale_model.browse(sale_id)
        self.assertEqual(sale.warehouse_id, self.warehouse)
