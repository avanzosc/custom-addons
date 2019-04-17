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
        self.product_model = self.env['product.product']
        self.sale_model = self.env['sale.order']
        self.pos_model = self.env['pos.order']
        self.session_model = self.env['pos.session']
        self.config_model = self.env['pos.config']
        self.wiz_pay_model = self.env['pos.make.payment']
        truke_product = self.env.ref('trukebai.product_product_truke')
        cond = [('state', '!=', 'closed')]
        self.pos_sessions = self.session_model.search(cond)
        self.pos_sessions.write({'state': 'closed'})
        self.truke_product = truke_product.copy()
        truke_product.unlink()
        cond = [('type', '=', 'sale')]
        pricelist = self.env['product.pricelist'].search(cond, limit=1)
        self.partner = self.env['res.partner'].create({
            'name': 'Partner test',
            'property_product_pricelist': pricelist.id})
        supplier_location = self.location_model.create({
            'usage': 'supplier',
            'name': 'Default Supplier Location'
        })
        internal_location = self.location_model.create({
            'usage': 'internal',
            'name': 'Default Internal Location'
        })
        self.picking_in_type = self.picking_type_model.create({
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
            'type': 'product',
        })
        self.picking_in = self.picking_model.create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_in_type.id
        })
        move_vals = {
            'name': product.name,
            'product_id': product.id,
            'product_uom': product.uom_id.id,
            'product_uom_qty': 15,
            'picking_id': self.picking_in.id,
            'picking_type_id': self.picking_in_type.id,
            'price_unit': 12,
            'truke_amount': 20,
            'location_id': self.picking_in_type.default_location_src_id.id,
            'location_dest_id':
            self.picking_in_type.default_location_dest_id.id,
            }
        self.move_in = self.env['stock.move'].create(move_vals)

    def test_picking_transfer_by_wizard(self):
        for move in self.picking_in.move_lines:
            move._compute_total_cost()
            self.assertEqual(
                move.product_uom_qty * move.price_unit, move.total_cost,
                'Bad cost in move line')
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

    def test_sale_order_trukebai(self):
        product_vals = {'name': 'Product for test truke',
                        'is_truke': False,
                        'max_trukes': 30}
        product = self.product_model.create(product_vals)
        out_type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        move_vals = {'name': self.truke_product.name,
                     'product_id': self.truke_product.id,
                     'product_uom': self.truke_product.uom_id.id,
                     'product_uom_qty': 20,
                     'partner_id': self.partner.id,
                     'location_id': out_type.default_location_src_id.id,
                     'location_dest_id': out_type.default_location_dest_id.id,
                     'state': 'done'}
        self.env['stock.move'].create(move_vals)
        self.assertEqual(
            self.partner.truke_balance, 20, 'Bad trukes for partner')
        sale_vals = {'name': 'Sale Order for test trukebai',
                     'partner_id': self.partner.id}
        sale_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'product_uom_qty': 1,
            'product_uom': product.uom_id.id,
            'price_unit': 2}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        sale_order = self.sale_model.create(sale_vals)
        sale_order.contributed_trukes = 50
        sale_order.onchange_contributed_trukes()
        self.assertEqual(
            sale_order.contributed_trukes, 20,
            'Bad Contributed trukes in sale order')
        sale_order.contributed_trukes = 2
        sale_order.action_button_confirm()
        self.assertEqual(
            len(sale_order.order_line), 2,
            'Product truke not found in sale order line')
        cond = [('origin', '=', sale_order.name)]
        picking = self.picking_model.search(cond)
        self.assertEqual(
            len(picking), 1, 'Out picking not found')
        self.assertEqual(
            len(picking.move_lines), 1, 'Bad lines in out picking')
        picking.force_assign()
        picking.action_done()
        self.assertEqual(
            len(picking.truke_picking_id), 1, 'In truke picking not found')
        self.assertEqual(
            self.partner.truke_balance, 18, 'Bad trukes(2) for partner')

    def test_pos_order_trukebai(self):
        tpv_picking_type = self.env.ref('point_of_sale.picking_type_posout')
        sale_journal = self.env.ref('account.sales_journal')
        bank_journal = self.env.ref('account.bank_journal')
        config_vals = {'name': 'Test TPV',
                       'picking_type_id': tpv_picking_type.id,
                       'stock_location_id':
                       tpv_picking_type.default_location_src_id.id,
                       'journal_id': sale_journal.id,
                       'iface_invoicing': True,
                       'journal_ids': [(6, 0, bank_journal.ids)]}
        config = self.config_model.create(config_vals)
        session_vals = {'user_id': self.env.user.id,
                        'state': 'opened',
                        'config_id': config.id}
        session = self.session_model.create(session_vals)
        product_vals = {'name': 'Product for test truke',
                        'is_truke': False,
                        'max_trukes': 30}
        product = self.product_model.create(product_vals)
        out_type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        move_vals = {'name': self.truke_product.name,
                     'product_id': self.truke_product.id,
                     'product_uom': self.truke_product.uom_id.id,
                     'product_uom_qty': 20,
                     'partner_id': self.partner.id,
                     'location_id': out_type.default_location_src_id.id,
                     'location_dest_id': out_type.default_location_dest_id.id,
                     'state': 'done'}
        self.env['stock.move'].create(move_vals)
        self.assertEqual(
            self.partner.truke_balance, 20, 'Bad trukes for partner')
        pos_vals = {'name': 'Pos Order for test trukebai',
                    'partner_id': self.partner.id,
                    'session_id': session.id,
                    'pricelist_id': self.partner.property_product_pricelist.id}
        pos_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'qty': 1,
            'price_unit': 2}
        pos_vals['lines'] = [(0, 0, pos_line_vals)]
        pos_order = self.pos_model.create(pos_vals)
        pos_order.contributed_trukes = 50
        pos_order.onchange_contributed_trukes()
        self.assertEqual(
            pos_order.contributed_trukes, 20,
            'Bad Contributed trukes in pos order')
        pos_order.session_id.write({'statement_ids': [(6, 0, [1])]})
        pos_order.session_id.statement_ids[0].journal_id = 1
        pos_order.contributed_trukes = 2
        wiz = self.wiz_pay_model.create(
            {'journal_id':
             pos_order.session_id.statement_ids[0].journal_id.id})
        wiz.with_context(active_id=pos_order.id).check()
        self.assertEqual(
            len(pos_order.lines), 2, 'Truke product not found in pos order')
        pos_order.picking_type_id.return_picking_type_id = False
        with self.assertRaises(exceptions.Warning):
            pos_order.create_picking()
        cond = [('code', '=', 'incoming')]
        in_picking_type = self.picking_type_model.search(cond, limit=1)
        pos_order.picking_type_id.return_picking_type_id = (
            in_picking_type.id)
        pos_order.create_picking()
        cond = [('origin', '=', pos_order.name),
                ('truke_picking_id', '!=', False)]
        picking = self.picking_model.search(cond, limit=1)
        self.assertEqual(
            len(picking), 1, 'Pos order out picking not found')
        self.assertEqual(
            len(picking.move_lines), 1, 'Bad lines in Pos order out picking')
        self.assertEqual(
            len(picking.truke_picking_id), 1,
            'Pos order in truke picking not found')
