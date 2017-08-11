# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def get_pack_lines(self):
        moves = self.move_lines.filtered(
            lambda x: x.procurement_id.sale_line_id and
            x.procurement_id.sale_line_id.product_id.id != x.product_id.id)
        return moves.mapped('procurement_id.sale_line_id')

    @api.multi
    def get_pack_line_moves(self, pack_line):
        return self.move_lines.filtered(
            lambda x: x.procurement_id.sale_line_id.id == pack_line.id)

    @api.multi
    @api.depends('move_lines', 'move_lines.product_qty',
                 'move_lines.product_uos_qty')
    def _amount_all(self):
        for picking in self:
            picking.amount_untaxed = 0.0
            picking.amount_total = 0.0
            val2 = val1 = val = 0.0
            sale_line_ids = []
            for line in picking.move_lines:
                if line.procurement_id and line.procurement_id.sale_line_id:
                    sale_line = line.procurement_id.sale_line_id
                    if sale_line.id in sale_line_ids:
                        continue
                    sale_line_ids += [sale_line.id]
                    cur = sale_line.order_id.pricelist_id.currency_id
                    price = sale_line.price_unit * (
                        1 - (sale_line.discount or 0.0) / 100.0)
                    taxes = sale_line.tax_id.compute_all(
                        price, line.product_qty,
                        sale_line.order_id.partner_invoice_id.id,
                        line.product_id, sale_line.order_id.partner_id)
                    val1 += cur.round(taxes['total'])
                    val += cur.round(taxes['total_included'])
                    for tax in taxes['taxes']:
                        val2 += tax.get('amount', 0.0)
            picking.amount_untaxed = val1
            picking.amount_tax = val2
            picking.amount_total = val

    @api.multi
    def compute(self, picking):
        if not picking.sale_id:
            return {}
        tax_grouped = {}
        order = picking.sale_id
        currency = order.currency_id.with_context(
            date=order.date_order or fields.Date.context_today(order))
        sale_line_ids = []
        for move in picking.move_lines:
            sale_line = move.procurement_id.sale_line_id
            if sale_line.id in sale_line_ids:
                continue
            sale_line_ids += [sale_line.id]
            price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) /
                                            100)
            taxes = sale_line.tax_id.compute_all(
                price, move.product_qty, move.product_id,
                picking.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'picking': picking.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'base': currency.round(tax['price_unit'] *
                                           move.product_qty),
                    'sequence': tax['sequence'],
                    'base_code_id': tax['base_code_id'],
                    'tax_code_id': tax['tax_code_id'],
                }
                key = (val['tax_code_id'], val['base_code_id'])
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
        return tax_grouped


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.depends('procurement_id', 'procurement_id.sale_line_id',
                 'procurement_id.sale_line_id.product_id', 'product_id',
                 'procurement_id.sale_line_id.price_unit', 'product_qty',
                 'procurement_id.sale_line_id.discount',
                 'procurement_id.sale_line_id.order_id.currency_id')
    def _compute_sale_prices(self):
        for record in self:
            sale_line = record.procurement_id.sale_line_id
            if sale_line and sale_line.product_id.id == record.product_id.id:
                record.sale_price_unit = sale_line.price_unit
                record.sale_discount = sale_line.discount
                currency = sale_line.order_id.currency_id
                record.sale_price_subtotal = currency.round(
                    (record.sale_price_unit * record.product_qty *
                     (1 - (record.sale_discount or 0.0) / 100.0)))
            else:
                record.sale_price_unit = 0
                record.sale_discount = 0
                record.sale_price_subtotal = 0

    sale_price_unit = fields.Float(
        string="Sale price unit", readonly=True, store=True,
        compute='_compute_sale_prices', related=False)
    sale_discount = fields.Float(
        string="Sale discount (%)", readonly=True, store=True,
        compute='_compute_sale_prices', related=False)
    sale_price_subtotal = fields.Float(
        string="Price subtotal", readonly=True, store=True,
        compute='_compute_sale_prices')
