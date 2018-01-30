# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _compute_sales_count(self):
        for product in self:
            product.repair_line_count = len(product.repair_line_ids)

    repair_line_ids = fields.One2many(
        comodel_name='mrp.repair.line', inverse_name='product_id',
        string='Repair line', domain=[('type', '=', 'add')])
    repair_line_count = fields.Integer(compute='_compute_sales_count')

    @api.multi
    def button_recompute_last_purchase_info(self):
        self._get_last_purchase()
