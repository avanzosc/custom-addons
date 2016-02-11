# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields


class TestTumakerCustom(common.TransactionCase):

    def setUp(self):
        super(TestTumakerCustom, self).setUp()
        self.analytic_model = self.env['account.analytic.account']
        self.analytic_line_model = self.env['account.analytic.line']
        self.purchase_model = self.env['purchase.order']
        self.purchase_line_model = self.env['purchase.order.line']
        self.invoice_model = self.env['account.invoice']
        self.location_obj = self.env['stock.location']
        self.partner_id = self.ref('base.res_partner_5')
        self.pricelist_id = self.ref('purchase.list0')
        analytic_vals = {
            'name': 'Analytic test',
            'type': 'normal',
            'quantity_max': 100,
            'partner_id': self.partner_id,
            'pricelist_id': self.pricelist_id,
            }
        self.analytic_id = self.analytic_model.create(analytic_vals)
        self.product_id = self.env.ref('product.product_product_6')
        acc = (self.product_id.property_account_expense.id or
               self.product_id.categ_id.property_account_expense_categ.id)
        analytic_line_vals = {
            'account_id': self.analytic_id.id,
            'name': 'Test line',
            'general_account_id': acc,
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

    def test_analytic_computed_vals(self):
        self.assertEqual(
            self.analytic_id.consumed_hours, 25,
            'Analytic invalid consumed hours')
        self.assertEqual(
            self.analytic_id.remaining_hours, 75,
            'Analytic invalid remaining hours')

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
