# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    manufacturer_id = fields.Many2one(
        related='product_id.manufacturer', string='Manufacturer', store=True)
    category_id = fields.Many2one(
        related='product_id.categ_id', string='Product category', store=True)
