# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contributed_trukes = fields.Integer(
        string='Contributed trukes', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    @api.onchange('contributed_trukes')
    def onchange_contributed_trukes(self):
        for sale in self:
            qty = sum(sale.mapped('order_line.max_trukes'))
            if sale.contributed_trukes > qty:
                sale.contributed_trukes = qty
            if sale.contributed_trukes > sale.partner_id.truke_balance:
                sale.contributed_trukes = sale.partner_id.truke_balance

    @api.multi
    def action_truke(self):
        self.ensure_one()
        self.mapped('order_line').filtered(
            lambda x: x.product_id.is_truke).unlink()
        if self.contributed_trukes <= 0:
            return True
        try:
            truke_product = self.env.ref('trukebai.product_product_truke')
        except Exception:
            truke_product = self.env['product.product'].search(
                [('is_truke', '=', True)], limit=1)
            if not truke_product:
                raise exceptions.Warning(_('Error! There is no a Truke '
                                           'product defined.'))
        line_vals = {
            'product_id': truke_product.id,
            'name': truke_product.name,
            'product_uom_qty': self.contributed_trukes,
            'product_uos_qty': self.contributed_trukes,
            'product_uom': truke_product.uom_id.id,
            'price_unit': 0,
            'sequence': max(self.mapped('order_line.sequence')) + 10,
            'order_id': self.id}
        self.env['sale.order.line'].create(line_vals)

    @api.multi
    def action_button_confirm(self):
        for sale in self:
            sale.action_truke()
        res = super(SaleOrder, self).action_button_confirm()
        for sale in self:
            line_truke = sale.mapped('order_line').filtered(
                lambda x: x.product_id.is_truke)
            if line_truke:
                sale.picking_ids[0].sale_line_truke_id = line_truke[0].id
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom_qty')
    def _compute_max_trukes(self):
        for line in self:
            line.max_trukes = line.product_id.max_trukes * line.product_uom_qty

    max_trukes = fields.Integer(
        string='Max trukes', compute='_compute_max_trukes', store=True)
