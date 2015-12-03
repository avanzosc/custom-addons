# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ProductMove(models.Model):
    _name = 'product.move'

    year = fields.Char('Year', size=4)
    incoming = fields.Integer('Incoming')
    outgoing = fields.Integer('Outgoing')
    product_id = fields.Many2one('product.product', 'Product')
