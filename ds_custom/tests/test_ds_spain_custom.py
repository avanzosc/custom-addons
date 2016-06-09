# -*- coding: utf-8 -*-
# © 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestDsCustom(common.TransactionCase):

    def setUp(self):
        super(TestDsCustom, self).setUp()
        self.product_product_model = self.env['product.product']
        self.product = self.browse_ref('product.product_product_3')
        group_portal_user = self.browse_ref('ds_custom.group_ds_portal_user')
        group_user = self.browse_ref('base.group_user')
        self.user = self.env['res.users'].create({
            'name': 'Portal user',
            'login': 'portal_user',
            'groups_id': [(6, 0, [group_user.id, group_portal_user.id])]
        })
