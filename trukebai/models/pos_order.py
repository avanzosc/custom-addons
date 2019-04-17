# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    contributed_trukes = fields.Integer(
        string='Contributed trukes', readonly=True,
        states={'draft': [('readonly', False)]})

    @api.onchange('contributed_trukes')
    def onchange_contributed_trukes(self):
        for pos in self.filtered(lambda x: x.partner_id):
            qty = sum(pos.mapped('lines.max_trukes'))
            if pos.contributed_trukes > qty:
                pos.contributed_trukes = qty
            if pos.contributed_trukes > pos.partner_id.truke_balance:
                pos.contributed_trukes = pos.partner_id.truke_balance

    @api.multi
    def action_truke(self):
        self.ensure_one()
        self.mapped('lines').filtered(
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
            'qty': self.contributed_trukes,
            'price_unit': 0,
            'order_id': self.id}
        self.env['pos.order.line'].create(line_vals)

    @api.multi
    def action_paid(self):
        for pos in self:
            pos.action_truke()
        return super(PosOrder, self).action_paid()


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    max_trukes = fields.Integer(
        string='Max trukes', related='product_id.max_trukes', readonly=True,
        store=True)
    move_id = fields.Many2one(
        comodel_name='stock.move', string='Stock move')
