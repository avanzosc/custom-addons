# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mrp_repair_ids = fields.One2many(
        comodel_name='mrp.repair', string='Mrp repairs',
        inverse_name='picking_out')
