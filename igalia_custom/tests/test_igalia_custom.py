# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields


class TestIgaliaCustom(common.TransactionCase):

    def setUp(self):
        super(TestIgaliaCustom, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.price_type_obj = self.env['product.price.type']
        self.pricelist_obj = self.env['product.pricelist']
        self.pricelist_version_obj = self.env['product.pricelist.version']
        self.analytic_line_obj = self.env['account.analytic.line']
        self.product = self.env.ref('product.product_product_6')
        self.asset_model = self.env['account.asset.asset']
        self.product.dollar_price = 75.0
        self.price_type = self.price_type_obj.create({
            'name': 'Dollar price',
            'field': 'dollar_price',
            'currency_id': self.ref('base.USD')})
        self.pricelist = self.pricelist_obj.create({
            'name': 'Dollar Pricelist',
            'currency_id': self.ref('base.USD'),
            'type': 'sale'})
        self.version = self.pricelist_version_obj.create({
            'name': 'Dollar Pricelist Version',
            'pricelist_id': self.pricelist.id})
        self.partner.property_product_pricelist = self.pricelist
        self.analytic_acc = self.env.ref('account.analytic_seagate_p2')
        self.analytic_acc.partner_id = self.partner
        self.analytic_acc.to_invoice = self.env.ref(
            'hr_timesheet_invoice.timesheet_invoice_factor1')
        self.general_acc = self.product.property_account_income or \
            self.product.categ_id.property_account_income_categ
        self.analytic_journal = self.ref('account.cose_journal_sale')
        analytic_line_vals = {
            'account_id': self.analytic_acc.id,
            'name': 'Test line',
            'journal_id': self.analytic_journal,
            'amount': 300,
            'general_account_id': self.general_acc.id,
            'product_id': self.product.id,
            'date': fields.Date.today()
            }
        self.analytic_line = self.analytic_line_obj.create(analytic_line_vals)
        asset_vals = {
            'name': 'Asset igalia custom',
            'category_id': self.ref('account_asset.account_asset_category_'
                                    'fixedassets0'),
            'code': 'REF01',
            'purchase_date': fields.Date.from_string('2015-01-01'),
            'method': 'linear',
            'purchase_value': 500,
            'method_time': 'number',
            'move_end_period': True,
            'method_number': 5,
            'method_period': 12
            }
        self.asset = self.asset_model.create(asset_vals)

    def test_pricelist(self):
        account_invoice = self.env.ref('account.invoice_1')
        account_invoice.partner_id = self.partner
        res = account_invoice.onchange_partner_id(
            'out_invoice', self.partner.id)
        self.assertEqual(res['value'].get('currency_id'),
                         self.partner.property_product_pricelist.currency_id)

    def test_analytic_line_invoice(self):
        res = self.analytic_line._prepare_cost_invoice_line(
            False, self.product.id, self.product.uom_id.id, self.env.uid,
            self.analytic_acc.to_invoice.id, self.analytic_acc,
            [self.analytic_line], 'general', {})
        acc = res.get('account_id', False)
        part_acc = self.partner.property_account_position.map_account(acc)
        self.assertEqual(acc, part_acc, "Account Not Correct")

    def test_product_id_change(self):
        acc_inv_vals = {
            'partner_id': self.partner.id,
            'payment_term': self.ref('account.account_payment_term'),
            'journal_id': self.ref('account.expenses_journal'),
            'currency_id': self.ref('base.EUR'),
            'reference_type': 'none',
            'company_id': self.ref('base.main_company'),
            'pricelist_id': self.pricelist.id,
            'type': 'out_invoice',
            'account_id': self.ref('account.a_recv')}
        acc_inv_line_vals = {
            'product_id': self.product.id,
            'account_id': self.ref('account.a_sale'),
            'quantity': 1,
            'name': 'Test',
            'price_unit': self.product.list_price
            }
        acc_inv_vals['invoice_line'] = [(0, 0, acc_inv_line_vals)]
        self.account_invoice = self.env['account.invoice'].create(acc_inv_vals)
        res = self.env['account.invoice.line'].product_id_change(
            self.product.id, self.product.uom_id.id, qty=1, type='out_invoice',
            partner_id=self.partner.id)
        self.assertEquals(self.partner.property_product_pricelist.price_get(
            self.product.id, 1.0, self.partner.id)[self.pricelist.id],
            res['value']['price_unit'])

    def test_asset(self):
        self.asset.compute_depreciation_board()
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.amount != 100)
        self.assertFalse(lines, "The amount of lines is not correct.")
        lines = self.asset.depreciation_line_ids.filtered(
            lambda x: x.method_percentage != 20)
        self.assertFalse(lines, "The percentage of lines is not correct.")
