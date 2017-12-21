# -*- coding: utf-8 -*-
# © 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(
        string='Cost Price', digits=dp.get_precision('Precision in sales'))
    list_price = fields.Float(
        string='Sale Price', digits=dp.get_precision('Precision in sales'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    base_lst_price = fields.Float(
        'Base Sale Price', digits=dp.get_precision('Precision in sales'))
    base_standard_price = fields.Float(
        'Base Cost Price', digits=dp.get_precision('Precision in sales'))
    lst_price = fields.Float(
        string='Public Price', digits=dp.get_precision('Precision in sales'))
    standard_price = fields.Float(
        string='Cost Price', digits=dp.get_precision('Precision in sales'))
