# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestUbarCustom(common.TransactionCase):

    def setUp(self):
        super(TestUbarCustom, self).setUp()
        self.product = self.browse_ref('product.product_product_6')
        self.product.old_reference = 'LA001'
        self.product_model = self.env['product.product']

    def test_name_search(self):
        product_ids = self.product_model.name_search(name='LA001', args=None)
        self.assertIn(self.product.id, ([a[0] for a in product_ids]),
                      'There is not any product with this old reference')
        product_ids = self.product_model.name_search('', args=None)
        all_product_ids = self.product_model.search('')
        self.assertEqual(len(product_ids), len(all_product_ids),
                         'Not the same quantity of products')

    def test_old_reference_change(self):
        message_count = len(self.product.message_ids)
        self.product.write({'old_reference': 'LA001'})
        self.assertEquals(len(self.product.message_ids), message_count,
                          "There must not have been created a new message.")
        self.product.write({'old_reference': 'LA002'})
        self.assertEquals(len(self.product.message_ids), message_count + 1,
                          "There must have been created a new message.")
