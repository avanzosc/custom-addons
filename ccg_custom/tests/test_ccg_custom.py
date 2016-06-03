# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestCCGCustom(common.TransactionCase):

    def setUp(self):
        super(TestCCGCustom, self).setUp()
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        self.packaging_obj = self.env['product.packaging']
        self.product_1 = self.env.ref('product.product_product_6')
        self.product_packaging1 = self.packaging_obj.create({
            'product_tmpl_id': self.product_1.product_tmpl_id.id,
            'ul': self.ref('product.product_ul_box'),
            'rows': 3,
            'is_default': True,
            })
        self.product = self.env.ref('product.product_product_18')
        self.product.route_ids = [
            (4, self.ref('mrp.route_warehouse0_manufacture')),
            (4, self.ref('stock.route_warehouse0_mto'))]

    def test_product_packaging_default(self):
        mrp_production_obj = self.env['mrp.production']
        mrp_production1 = mrp_production_obj.create({
            'product_id': self.product_1.id,
            'product_uom': self.ref('product.product_uom_unit'),
            'product_qty': 1,
            })
        res = mrp_production_obj.product_id_change(
            mrp_production1.product_id.id, mrp_production1.product_qty)
        self.assertEqual(
            res['value']['product_packaging'], self.product_packaging1.id,
            'Product packaging are not the same')

    def test_mo_vals(self):
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28'}
        self.account = self.account_model.create(account_vals)
        project_vals = {'name': 'project 1',
                        'analytic_account_id': self.account.id}
        self.project = self.project_model.create(project_vals)
        self.sale_order = self.env['sale.order'].create(
            {'partner_id': self.ref('base.res_partner_2'),
             'project_id': self.account.id})
        vals = {
            'order_id': self.sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 2,
            'product_uos_qty': 2,
            'product_uom': self.ref('product.product_uom_unit'),
            }
        self.sale_order.order_line = [(0, 0, vals)]
        self.sale_order.action_button_confirm()
        procurements = self.sale_order.mapped(
            'order_line.procurement_ids.group_id.procurement_ids')
        for procurement in procurements.filtered(
                lambda x: x.state == 'confirmed'):
            procurement.run()
        productions = procurements.mapped('production_id')
        for production in productions:
            self.assertEqual(production.sale_order_id, self.sale_order)
            self.assertEqual(production.partner_id, self.sale_order.partner_id)
