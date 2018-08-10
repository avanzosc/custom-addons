# -*- coding: utf-8 -*-
# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.htm

from openerp import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def do_transfer(self):
        res = super(StockPicking, self).do_transfer()
        repair_obj = self.env['mrp.repair']
        repair_line_obj = self.env['mrp.repair.line']
        for picking in self.filtered(
                lambda x: x.picking_type_id.code == 'incoming'):
            for move_line in picking.move_lines.filtered(
                    'purchase_line_id.account_analytic_id'):
                repair = repair_obj.search(
                    [('analytic_account', '=',
                      move_line.purchase_line_id.account_analytic_id.id),
                     ('state', 'not in', ('cancel', 'done'))])
                if repair and move_line.product_id.type != 'service':
                    line_values = repair_line_obj.product_id_change(
                        repair[0].pricelist_id.id, move_line.product_id.id,
                        uom=move_line.product_uom.id,
                        partner_id=move_line.purchase_line_id.partner_id.id
                        )['value']
                    line_values.update({
                        'product_id': move_line.product_id.id,
                        'repair_id': repair[0].id,
                        'user_id': self.env.user.id,
                        'type': 'add',
                        'product_uom_qty': move_line.product_uom_qty,
                        'expected_qty': move_line.product_uom_qty,
                        'location_id': repair[0].location_id.id,
                        'location_dest_id': repair[0].location_dest_id.id,
                        'tax_id': [(6, 0, 'tax_id' in line_values and
                                    line_values['tax_id'] or [])],
                    })
                    repair_line_obj.create(line_values)
        return res
