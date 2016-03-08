# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestIgaliaCustom(common.TransactionCase):

    def setUp(self):
        super(TestIgaliaCustom, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.price_type_obj = self.env['product.price.type']
        self.pricelist_obj = self.env['product.pricelist']
        self.pricelist_version_obj = self.env['product.pricelist.version']
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

    def test_pricelist(self):
        account_invoice = self.env.ref('account.invoice_1')
        account_invoice.partner_id = self.partner
        res = account_invoice.onchange_partner_id(
            'out_invoice', self.partner.id)
        self.assertEqual(res['value'].get('currency_id'),
                         self.partner.property_product_pricelist.currency_id)
