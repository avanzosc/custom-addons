# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _prepare_values_extra_move(self, op, product, remaining_qty):
        res = super(StockPicking, self)._prepare_values_extra_move(
            op, product, remaining_qty)
        purchase_line = op.mapped(
            'linked_move_operation_ids.move_id.purchase_line_id')
        res['purchase_line_id'] = purchase_line[:1].id
        return res


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    _order = "inventory_id, location_name, product_name, prodlot_name"


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.depends('purchase_line_id.discount',
                 'purchase_line_id.price_unit',
                 'product_uom_qty')
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = (
                record.purchase_line_id.price_unit * record.product_uom_qty *
                (1 - (record.purchase_line_id.discount/100)))

    price_subtotal = fields.Float(compute="_compute_price_subtotal",
                                  string="Subtotal", store=True)

    analytic_account = fields.Many2one(
        comodel_name='account.analytic.account',
        related='purchase_line_id.account_analytic_id',
        string='Analytic account', store=True)
    purchase_discount = fields.Float(string="Discount",
                                     related="purchase_line_id.discount")
    purchase_price_unit = fields.Float(string="Price Unit",
                                       related="purchase_line_id.price_unit")
    date_done = fields.Datetime(string="Date done", store=True,
                                related="picking_id.date_done")
