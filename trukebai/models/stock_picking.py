# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions, _
from openerp.tools.float_utils import float_compare
import openerp.addons.decimal_precision as dp


class StockPackOperation(models.Model):

    _inherit = 'stock.pack.operation'

    move_src_id = fields.Many2one(comodel_name='stock.move', string='Source')


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.depends('product_id', 'product_id.is_truke', 'product_qty',
                 'move_dest_id', 'location_id')
    def _compute_truke_qty(self):
        for move in self:
            move.truke_qty = 0
            if (move.product_id.is_truke and
                    move.location_dest_id.usage == 'customer'):
                move.truke_qty = move.product_qty
            if (move.product_id.is_truke and
                    move.location_id.usage == 'supplier'):
                move.truke_qty = move.product_qty * -1

    @api.multi
    @api.depends('product_uom_qty', 'price_unit')
    def _compute_total_cost(self):
        for move in self:
            move.total_cost = move.product_uom_qty * move.price_unit

    truke_amount = fields.Integer(string='Truke Amount')
    truke_qty = fields.Integer(
        string='Truke qty', compute='_compute_truke_qty', store=True)
    total_cost = fields.Float(
        string='Total cost', compute='_compute_total_cost',
        digits_compute=dp.get_precision('Product Price'), store=True)

    @api.model
    def create(self, values):
        sequence = self.env.ref('point_of_sale.seq_picking_type_posout')
        move = super(StockMove, self).create(values)
        if (move.picking_id and move.picking_type_id and
            move.picking_type_id.code == 'outgoing' and
            move.picking_type_id.sequence_id.id == sequence.id and
                move.product_id.is_truke):
            order = self.env['pos.order'].search(
                [('name', '=', move.picking_id.origin)], limit=1)
            if order:
                line_truke = order.mapped('lines').filtered(
                    lambda x: x.product_id.is_truke and
                    x.product_id.id == move.product_id.id)
                if line_truke:
                    line_truke[0].move_id = move.id
        return move

    @api.onchange('picking_id')
    def onchange_picking(self):
        self.ensure_one()
        self.partner_id = self.picking_id.partner_id

    @api.multi
    def action_confirm(self):
        moves = self._find_moves_not_truke()
        super(StockMove, moves).action_confirm()
        return self.ids

    def _find_moves_not_truke(self):
        sale_obj = self.env['sale.order']
        moves = self.env['stock.move']
        sequence = self.env.ref('point_of_sale.seq_picking_type_posout')
        for move in self.filtered(
            lambda x: not x.picking_type_id or
            (x.picking_type_id and x.picking_type_id.code == 'outgoing' and
             x.picking_type_id.sequence_id.id != sequence.id)):
            if (not move.product_id.is_truke or
                (move.product_id.is_truke and
                 (not move.origin or
                  (move.origin and len(
                    sale_obj.search([('name', '=', move.origin)],
                                    limit=1)) == 0)))):
                moves += move
        for move in self.filtered(
            lambda x: x.picking_type_id and
                x.picking_type_id.code == 'incoming'):
            moves += move
        for move in self.filtered(
            lambda x: x.picking_type_id and
            x.picking_type_id.code == 'outgoing' and
            x.picking_type_id.sequence_id.id == sequence.id and not
                x.product_id.is_truke):
            moves += move
        pos_move_truke = self.filtered(
            lambda x: x.picking_type_id and
            x.picking_type_id.code == 'outgoing' and
            x.picking_type_id.sequence_id.id == sequence.id and
            x.product_id.is_truke)
        pos_move_truke.write({'picking_id': False})
        return moves


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    truke_picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Truke Picking')
    sale_line_truke_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale line with truke product')
    pos_line_truke_id = fields.Many2one(
        comodel_name='pos.order.line',
        string='Pos Sale line with truke product')

    @api.multi
    def needs_outgoing_truke_picking(self):
        self.ensure_one()
        if self.picking_type_id.code == 'incoming' and \
                sum([x.truke_amount for x in self.move_lines]) > 0:
            return True
        return False

    @api.multi
    def needs_incoming_truke_picking(self):
        self.ensure_one()
        sequence = self.env.ref('point_of_sale.seq_picking_type_posout')
        if (self.origin and self.picking_type_id.code == 'outgoing' and
                self.picking_type_id.sequence_id.id == sequence.id):
            order = self.env['pos.order'].search(
                [('name', '=', self.origin)], limit=1)
            if order:
                line_truke = order.mapped('lines').filtered(
                    lambda x: x.product_id.is_truke)
                if line_truke and order.picking_id:
                    order.picking_id.pos_line_truke_id = line_truke[0].id
                    return True
        if (self.sale_line_truke_id or
            (self.picking_type_id.code == 'outgoing' and
             sum([x.truke_amount for x in self.move_lines]) > 0)):
            return True
        return False

    @api.multi
    def create_and_process_outgoing_truke_picking(self):
        self.ensure_one()
        picking_type = self._find_picking_type_for_trukes(
            'outgoing', self.move_lines[:1].location_dest_id.id)
        truke_product = self._find_truke_product_for_trukes()
        move_vals = self._create_move_vals_for_trukes(
            picking_type, truke_product)
        picking_vals = {
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'picking_type_id': picking_type.id,
            'move_lines': [(0, 0, move_vals)]
            }
        truke_picking = self.create(picking_vals)
        self.truke_picking_id = truke_picking.id
        self._terminate_with_truke_picking(truke_picking)

    @api.multi
    def create_and_process_incoming_truke_picking(self):
        if not self.picking_type_id.return_picking_type_id:
            raise exceptions.Warning(
                _('Picking type for returns not found, for picking type: %s') %
                self.picking_type_id.name)
        return_picking_type = self.picking_type_id.return_picking_type_id
        picking_vals = {'partner_id': self.partner_id.id,
                        'origin': self.name,
                        'picking_type_id': return_picking_type.id}
        if sum([x.truke_amount for x in self.move_lines]) > 0:
            truke_product = self._find_truke_product_for_trukes()
            move_vals = self._create_move_vals_for_trukes(
                return_picking_type, truke_product)
            move_vals['picking_type_id'] = return_picking_type.id
            picking_vals['move_lines'] = [(0, 0, move_vals)]
        else:
            if self.sale_line_truke_id:
                truke_move = (
                    self.sale_line_truke_id.procurement_ids[0].move_ids[0])
            else:
                truke_move = self.pos_line_truke_id.move_id
            truke_move.write(
                {'picking_type_id': return_picking_type.id,
                 'location_id': return_picking_type.default_location_src_id.id,
                 'location_dest_id':
                 return_picking_type.default_location_dest_id.id})
            picking_vals['move_lines'] = [(6, 0, truke_move.ids)]
        truke_picking = self.create(picking_vals)
        self.truke_picking_id = truke_picking.id
        self._terminate_with_truke_picking(truke_picking)

    @api.multi
    def _find_picking_type_for_trukes(self, code, location_id):
        cond = [('code', '=', code)]
        if code == 'outgoing':
            cond.append(('default_location_src_id', '=', location_id))
        else:
            cond.append(('default_location_dest_id', '=', location_id))
        picking_type = self.env['stock.picking.type'].search(cond, limit=1)
        return picking_type

    @api.multi
    def _find_truke_product_for_trukes(self):
        try:
            truke_product = self.env.ref('trukebai.product_product_truke')
        except:
            truke_product = self.env['product.product'].search(
                [('is_truke', '=', True)], limit=1)
            if not truke_product:
                raise exceptions.Warning(_('Error! There is no a Truke '
                                           'product defined.'))
        return truke_product

    @api.multi
    def _create_move_vals_for_trukes(self, picking_type, truke_product):
        move_vals = {
            'name': truke_product.name,
            'partner_id': self.partner_id.id,
            'product_id': truke_product.id,
            'product_uom': truke_product.uom_id.id,
            'product_uom_qty': sum([x.truke_amount for x in self.move_lines]),
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            }
        return move_vals

    def _terminate_with_truke_picking(self, picking):
        picking.action_confirm()
        picking.force_assign()
        picking.action_done()

    @api.multi
    def action_done(self):
        for record in self:
            if record.needs_outgoing_truke_picking():
                record.create_and_process_outgoing_truke_picking()
            if record.needs_incoming_truke_picking():
                record.create_and_process_incoming_truke_picking()
        return super(StockPicking, self).action_done()

    @api.multi
    def do_transfer(self):
        for record in self:
            if record.needs_outgoing_truke_picking():
                record.create_and_process_outgoing_truke_picking()
            if record.needs_incoming_truke_picking():
                record.create_and_process_incoming_truke_picking()
        return super(StockPicking, self).do_transfer()

    @api.model
    def _prepare_pack_ops(self, picking, quants, forced_qties):
        res = []
        for move_line in picking.move_lines:
            forced_qties = {}
            picking_quants = []
            if move_line.state not in ('assigned', 'confirmed', 'waiting'):
                continue
            picking_quants = move_line.mapped('reserved_quant_ids')
            forced_qty = ((move_line.state == 'assigned') and
                          move_line.product_qty -
                          sum([x.qty for x in picking_quants]) or 0)
            if float_compare(
                    forced_qty, 0,
                    precision_rounding=move_line.product_uom.rounding) > 0:
                forced_qties[move_line.product_id] = forced_qty
            move_packs = super(StockPicking, self)._prepare_pack_ops(
                picking, picking_quants, forced_qties)
            for line in move_packs:
                line['move_src_id'] = move_line.id
            res += move_packs
        return res

    @api.multi
    def do_print_receipt(self):
        self.ensure_one()
        report = self.env['report'].get_action(
            self, 'trukebai.picking_receipt_report')
        del report['report_type']
        return report

    @api.multi
    def do_print_product_label(self):
        self.ensure_one()
        report = self.env['report'].get_action(
            self, 'trukebai.product_label_report')
        del report['report_type']
        return report

    @api.multi
    def get_total_partner_truke(self):
        self.ensure_one()
        return self.partner_id.truke_balance

    @api.multi
    def get_awarded_truke(self):
        self.ensure_one()
        return sum(self.mapped('move_lines.truke_amount'))
