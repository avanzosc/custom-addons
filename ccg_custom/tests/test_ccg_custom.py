# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestCCGCustom(common.TransactionCase):

    def setUp(self):
        super(TestCCGCustom, self).setUp()
        self.packaging_obj = self.env['product.packaging']
        self.product_packaging1 = self.packaging_obj.create({
            'product_tmpl_id': self.ref('product.product_product_6'),
            'ul': self.ref('product.product_ul_box'),
            'rows': 3,
            'is_default': True,
            })

    def test_product_packaging_default(self):
        self.mrp_production_obj = self.env['mrp.production']
        self.mrp_production1 = self.mrp_production_obj.create({
            'product_id': self.ref('product.product_product_6'),
            'product_uom': self.ref('product.product_uom_unit')
            })
        self.assertEqual(
            self.mrp_production1.product_packaging, self.product_packaging1,
            'Product packaging are not the same')
