# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestTumakerPickingReport(common.TransactionCase):

    def setUp(self):
        super(TestTumakerPickingReport, self).setUp()
        self.product_model = self.env['product.product']
        self.partner1 = self.env.ref('base.res_partner_2')
        self.product_bom = self.product_model.create(
            {'name': 'Avanzosc'})
        self.product_bom1 = self.product_model.create(
            {'name': 'Pieza 1'})
        self.product_bom1.qty_available = 360.0
        self.product_bom2 = self.product_model.create(
            {'name': 'Pieza 2'})
        self.product_bom2.qty_available = 320.0
        self.mrp_bom_values = {
            'product_tmpl_id': self.product_bom.product_tmpl_id.id,
            'product_id': self.product_bom.id,
            'type': 'phantom'}
        self.mrp_bom_line1 = {
            'product_id': self.product_bom1.id,
            'product_qty': 3.0}
        self.mrp_bom_line2 = {
            'product_id': self.product_bom2.id,
            'product_qty': 2.0}
        self.mrp_bom_values['bom_line_ids'] = ([(0, 0, self.mrp_bom_line1),
                                                (0, 0, self.mrp_bom_line2)])
        self.mrp_bom_product = self.env['mrp.bom'].create(self.mrp_bom_values)
        self.sale_values = {
            'partner_id': self.partner1.id,
            'order_policy': 'manual'}
        self.line1_values = {
            'product_id': self.product_bom.id,
            'product_uom_qty': 2,
            'product_uom': self.product_bom.uom_id.id,
        }

    def test_pack_product_sale(self):
        self.sale_order = self.env['sale.order'].create(self.sale_values)
        self.line1_values.update(self.env['sale.order.line'].product_id_change(
            self.sale_order.pricelist_id.id, self.product_bom.id, qty=2,
            uom=self.product_bom.uom_id.id, qty_uos=2,
            uos=self.product_bom.uom_id.id, partner_id=self.partner1.id
            ).get('value', {}))
        self.line1_values.update({'price_unit': 50})
        self.sale_order.order_line = [(0, 0, self.line1_values)]
        self.sale_order.action_button_confirm()
        picking = self.sale_order.picking_ids[:1]
        picking.compute(picking)
        picking.move_lines[0].product_uom_qty = 2
        self.assertEqual(picking.amount_untaxed, 100)
        for move in picking.move_lines:
            self.assertEqual(move.sale_price_unit, 0)
            self.assertEqual(move.sale_price_subtotal, 0)
        self.assertTrue(self.sale_order.order_line[:1].id in
                        picking.get_pack_lines().ids)
        for move in picking.move_lines:
            self.assertTrue(move.id in picking.get_pack_line_moves(
                self.sale_order.order_line[:1]).ids)

    def test_not_pack_product_sale(self):
        self.sale_order = self.env['sale.order'].create(self.sale_values)
        self.line1_values.update({'product_id': self.product_bom2.id,
                                  'price_unit': 50})
        self.sale_order.order_line = [(0, 0, self.line1_values)]
        self.sale_order.action_button_confirm()
        picking = self.sale_order.picking_ids[:1]
        picking.compute(picking)
        self.assertEqual(picking.amount_untaxed, 100)
        for move in picking.move_lines:
            self.assertEqual(move.sale_price_unit, 50)
            self.assertEqual(move.sale_price_subtotal, 100)
        self.assertFalse(picking.get_pack_lines())
