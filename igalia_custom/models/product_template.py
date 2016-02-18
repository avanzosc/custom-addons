# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dollar_price = fields.Float(string='Price in dollars')
