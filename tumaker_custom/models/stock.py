# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _prepare_values_extra_move(self, op, product, remaining_qty):
        res = super(StockPicking, self)._prepare_values_extra_move(
            op, product, remaining_qty)
        purchase_line = op.mapped(
            'linked_move_operation_ids.move_id.purchase_line_id')
        res['purchase_line_id'] = purchase_line.id
        return res


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    _order = "inventory_id, location_name, product_name, prodlot_name"
