# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Order Line',
        ondelete='set null', select=True, readonly=True)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    @api.depends('account_analytic_ids.quant_id')
    def _compute_to_invoice(self):
        for line in self:
            account = line.account_analytic_ids.filtered(
                lambda x: x.date < fields.Date.today() and x.state == 'open')
            line.to_invoice = account[:1].remaining_ca or 0.0

    manufacturer_id = fields.Many2one(
        related='product_id.manufacturer', string='Manufacturer', store=True)
    category_id = fields.Many2one(
        related='product_id.categ_id', string='Product category', store=True)
    account_analytic_ids = fields.One2many(
        comodel_name='account.analytic.account', inverse_name='quant_id',
        string='Account Analytic')
    to_invoice = fields.Float(compute='_compute_to_invoice')


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    account_analytic_ids = fields.One2many(
        comodel_name='account.analytic.account', string='Anaylitic account',
        inverse_name='lot_id')
