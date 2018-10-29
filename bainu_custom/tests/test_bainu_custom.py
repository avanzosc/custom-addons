# -*- coding: utf-8 -*-
# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestBainuCustom(common.TransactionCase):

    def setUp(self):
        super(TestBainuCustom, self).setUp()
        self.crm_wiz_obj = self.env['crm.make.sale']
        self.crm_lead_obj = self.env['crm.lead']
        self.sale_line_model = self.env['sale.order.line']
        self.sale_obj = self.env['sale.order']
        self.stage = self.env.ref('crm.stage_lead6')
        self.stockable_product = self.env.ref('product.product_product_3')
        lead_vals = {
            'name': 'Test Opportunity',
            'partner_id': self.ref('base.res_partner_1'),
            }
        self.lead = self.crm_lead_obj.create(lead_vals)
        self.sale_line_vals = {
            'product_id': self.stockable_product.id,
            'name': self.stockable_product.name,
            'product_uos_qty': 7,
            'product_uom': self.stockable_product.uom_id.id,
            'price_unit': self.stockable_product.list_price}

    def test_sale_order(self):
        self.assertNotEqual(self.lead.stage_id.id, self.stage.id,
                            "Stage is not correct")
        wiz = self.crm_wiz_obj.create(
            {'partner_id': self.ref('base.res_partner_1')})
        result = wiz.with_context(active_ids=[self.lead.id]).makeOrder()
        self.sale_line_vals['order_id'] = result['res_id']
        self.sale_line_model.create(self.sale_line_vals)
        sale_order = self.sale_obj.browse(result['res_id'])
        sale_order.action_button_confirm()
        self.assertEqual(self.lead.stage_id.id, self.stage.id,
                         "Stage is not correct")
