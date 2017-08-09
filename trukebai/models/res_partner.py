# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    @api.depends('truke_moves', 'truke_moves.product_qty',
                 'truke_moves.location_id', 'truke_moves.location_dest_id',
                 'truke_moves.location_id.usage',
                 'truke_moves.location_dest_id.usage')
    def _compute_truke_balance(self):
        for record in self:
            incoming = sum([
                x.product_qty for x in record.truke_moves.filtered(
                    lambda x: x.location_dest_id.usage == 'customer')])
            outgoing = sum([
                x.product_qty for x in record.truke_moves.filtered(
                    lambda x: x.location_id.usage == 'customer')])
            record.truke_balance = int(incoming - outgoing)

    truke_balance = fields.Integer(
        string='Truke Balance', compute='_compute_truke_balance', store=True)
    truke_moves = fields.One2many(
        comodel_name='stock.move', inverse_name='partner_id',
        domain=[('product_id.is_truke', '=', True), ('state', '=', 'done')])
