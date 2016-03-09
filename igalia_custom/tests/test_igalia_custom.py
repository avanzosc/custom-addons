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
