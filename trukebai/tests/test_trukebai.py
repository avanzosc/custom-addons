# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import exceptions
import openerp.tests.common as common


class TestTrukebai(common.TransactionCase):

    def setUp(self):
        super(TestTrukebai, self).setUp()
        self.wiz_obj = self.env['stock.transfer_details']
        self.location_model = self.env['stock.location']
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        truke_product = self.env.ref('trukebai.product_product_truke')
        self.truke_product = truke_product.copy()
        truke_product.unlink()
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test'
        })
        supplier_location = self.location_model.create({
            'usage': 'supplier',
            'name': 'Default Supplier Location'
        })
        internal_location = self.location_model.create({
            'usage': 'internal',
            'name': 'Default Internal Location'
        })
        picking_in_type = self.picking_type_model.create({
            'name': 'Incoming picking type',
            'code': 'incoming',
            'sequence_id': self.ref('stock.seq_type_picking_in'),
            'default_location_dest_id': internal_location.id,
            'default_location_src_id': supplier_location.id,
            })
        self.picking_out_type = self.picking_type_model.create({
            'name': 'Outgoing picking type',
            'code': 'outgoing',
            'sequence_id': self.ref('stock.seq_type_picking_out'),
            'default_location_src_id': internal_location.id,
            'default_location_dest_id': supplier_location.id,
            })
        product = self.env['product.product'].create({
            'name': 'Test Transfer Cancel Product',
            'type': 'product'
        })
        self.picking_in = self.picking_model.create({
            'partner_id': self.partner.id,
            'picking_type_id': picking_in_type.id
        })
        move_vals = {
            'name': product.name,
            'product_id': product.id,
            'product_uom': product.uom_id.id,
            'product_uom_qty': 15,
            'picking_id': self.picking_in.id,
            'price_unit': 12,
            'truke_amount': 20,
            'location_id': picking_in_type.default_location_src_id.id,
            'location_dest_id': picking_in_type.default_location_dest_id.id,
            }
        self.move_in = self.env['stock.move'].create(move_vals)

    def test_picking_transfer_by_wizard(self):
        self.picking_in.action_confirm()
        self.picking_in.action_assign()
        self.assertEqual(self.picking_in.state, 'assigned')
        res = self.picking_in.do_enter_transfer_details()
        wizard = self.wiz_obj.browse(res.get('res_id'))
        wizard.item_ids[0].truke_amount = 23
        wizard.item_ids[0].price_unit = 55.20
        self.assertEqual(self.move_in.truke_amount, 23)
        self.assertEqual(self.move_in.price_unit, 55.20)
        wizard.do_detailed_transfer()
        self.assertEqual(self.picking_in.state, 'done')
        self.assertTrue(self.picking_in.truke_picking_id)
        self.assertEqual(self.picking_in.truke_picking_id.picking_type_id,
                         self.picking_out_type)
        self.assertEqual(
            self.picking_in.truke_picking_id.move_lines[0].product_qty, 23)

    def test_picking_transfer_by_force(self):
        self.picking_in.action_confirm()
        self.picking_in.force_assign()
        self.truke_product.is_truke = False
        with self.assertRaises(exceptions.Warning):
            self.picking_in.action_done()
        self.truke_product.is_truke = True
        self.picking_in.action_done()
        self.partner.invalidate_cache()
        self.assertEqual(self.picking_in.state, 'done')
        self.assertTrue(self.picking_in.truke_picking_id)
        self.assertEqual(
            self.picking_in.truke_picking_id.move_lines[0].product_qty, 20)
        self.assertTrue(
            self.picking_in.truke_picking_id.move_lines[0].product_id.is_truke)
        self.assertTrue(
            self.picking_in.truke_picking_id.move_lines[0].id in
            self.partner.truke_moves.ids)
        self.partner.truke_moves[:1].location_dest_id.usage = 'customer'
        self.assertEqual(self.partner.truke_balance, 20)
        res = self.picking_in.do_print_receipt()
        self.assertEqual(res.get('type'), 'ir.actions.report.xml')
        res = self.picking_in.do_print_product_label()
        self.assertEqual(res.get('type'), 'ir.actions.report.xml')
