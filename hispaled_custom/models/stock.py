# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    @api.depends('group_id')
    def _compute_sale_order_id(self):
        for picking in self.filtered(
                lambda x: x.code == 'outgoing'):
            cond = [('procurement_group_id', '=', picking.group_id.id)]
            sale = self.env['sale.order'].search(cond, limit=1)
            if sale:
                picking.sale_order_id = sale.id

    code = fields.Selection(
        string='Code', related='picking_type_id.code', store=True)
    sale_order_id = fields.Many2one(
        string='Sale order', store=True, comodel_name='sale.order',
        compute='_compute_sale_order_id')
    client_order_ref = fields.Char(
        string='Sale order Reference/Description', store=True,
        related='sale_order_id.client_order_ref')
    project_id = fields.Many2one(
        string='Project', comodel_name='account.analytic.account',
        related='sale_order_id.project_id', store=True)
    packaging_comment = fields.Text(
        string='Packaging comment', translate=True)

    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        if picking.sale_order_id:
            vals['sale_order_id'] = picking.sale_order_id.id
        return super(StockPicking, self)._create_invoice_from_picking(
            picking, vals)


class StockMove(models.Model):
    _inherit = 'stock.move'

    name = fields.Text(string='Description', required=True)

    @api.multi
    def onchange_product_id(self, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        result = super(StockMove, self).onchange_product_id(
            prod_id=prod_id, loc_id=loc_id, loc_dest_id=loc_dest_id,
            partner_id=partner_id)
        if prod_id and result.get('value', False):
            p = self.env['product.product'].browse(prod_id)
            if p.variant_description:
                result['value']['name'] = p.variant_description
        return result
