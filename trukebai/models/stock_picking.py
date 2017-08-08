# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare


class StockPackOperation(models.Model):

    _inherit = 'stock.pack.operation'

    move_src_id = fields.Many2one(comodel_name='stock.move', string='Source')


class StockMove(models.Model):

    _inherit = 'stock.move'

    truke_amount = fields.Integer(string='Truke Amount')

    @api.onchange('picking_id')
    def onchange_picking(self):
        self.ensure_one()
        self.partner_id = self.picking_id.partner_id


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    truke_picking_id = fields.Many2one(comodel_name='stock.picking',
                                       string='Truke Picking')

    @api.multi
    def needs_outgoing_truke_picking(self):
        self.ensure_one()
        if self.picking_type_id.code == 'incoming' and \
                sum([x.truke_amount for x in self.move_lines]) > 0:
            return True
        return False

    @api.multi
    def create_and_process_outgoing_truke_picking(self):
        self.ensure_one()
        location_id = self.move_lines[:1].location_dest_id.id
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('default_location_src_id', '=', location_id)], limit=1)
        try:
            truke_product = self.env.ref('trukebai.product_product_truke')
        except:
            truke_product = self.env['product.product'].search(
                [('is_truke', '=', True)], limit=1)
        move_vals = {
            'name': truke_product.name,
            'partner_id': self.partner_id.id,
            'product_id': truke_product.id,
            'product_uom': truke_product.uom_id.id,
            'product_uom_qty': sum([x.truke_amount for x in self.move_lines]),
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            }
        picking_vals = {
            'partner_id': self.partner_id.id,
            'origin': self.name,
            'picking_type_id': picking_type.id,
            'move_lines': [(0, 0, move_vals)]
            }
        self.truke_picking_id = self.create(picking_vals)
        self.truke_picking_id.action_confirm()
        self.truke_picking_id.force_assign()
        self.truke_picking_id.action_done()

    @api.multi
    def action_done(self):
        for record in self:
            if record.needs_outgoing_truke_picking():
                record.create_and_process_outgoing_truke_picking()
        return super(StockPicking, self).action_done()

    @api.multi
    def do_transfer(self):
        for record in self:
            if record.needs_outgoing_truke_picking():
                record.create_and_process_outgoing_truke_picking()
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
