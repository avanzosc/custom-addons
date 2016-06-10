# -*- coding: utf-8 -*-
# © 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models
import openerp.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    base_lst_price = fields.Float(
        'Base Sale Price', digits_compute=dp.get_precision('Product Price'))
    base_standard_price = fields.Float(
        'Base Cost Price', digits_compute=dp.get_precision('Product Price'))
