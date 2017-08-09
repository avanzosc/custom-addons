# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockTransferDetails(models.TransientModel):

    _inherit = 'stock.transfer_details'

    @api.model
    def default_get(self, fields):
        items = []
        res = super(StockTransferDetails, self).default_get(fields)
        picking_id = self.env.context.get('active_id', False)
        if not picking_id:
            return res
        picking = self.env['stock.picking'].browse(picking_id)
        if not picking.pack_operation_ids:
            picking.do_prepare_partial()
        for op in picking.pack_operation_ids.filtered(lambda x: x.product_id):
            items.append({
                'packop_id': op.id,
                'product_id': op.product_id.id,
                'product_uom_id': op.product_uom_id.id,
                'quantity': op.product_qty,
                'package_id': op.package_id.id,
                'lot_id': op.lot_id.id,
                'sourceloc_id': op.location_id.id,
                'destinationloc_id': op.location_dest_id.id,
                'result_package_id': op.result_package_id.id,
                'date': op.date,
                'owner_id': op.owner_id.id,
                'move_src_id': op.move_src_id.id,
            })
        res.update(item_ids=items)
        return res

    @api.multi
    def do_detailed_transfer(self):
        self.ensure_one()
        res = super(StockTransferDetails, self).do_detailed_transfer()
        if self.picking_id.picking_type_id.code == 'incoming':
            return self.picking_id.do_print_receipt()
        return res


class StockTransferDetailsItems(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    move_src_id = fields.Many2one(comodel_name='stock.move', string='Source')
    price_unit = fields.Float(related='move_src_id.price_unit')
    truke_amount = fields.Integer(related='move_src_id.truke_amount')
