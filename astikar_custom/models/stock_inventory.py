# -*- coding: utf-8 -*-
# © 2022 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.multi
    def action_open_inventory_lines(self):
        res = super(StockInventory, self).action_open_inventory_lines()
        view_id = self.env.ref(
            'astikar_custom.stock_inventory_line_tree')
        res['view_id'] = view_id.id
        res['views'] = [(view_id.id, u'tree')]
        return res

class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    categ_id = fields.Many2one(
        comodel_name="product.category", string="Category",
        related="product_id.categ_id")
    product_type = fields.Selection(related="product_id.type", string="Type")