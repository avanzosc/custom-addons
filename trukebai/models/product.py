# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    is_truke = fields.Boolean(string="Is Truke")
    max_trukes = fields.Integer(string='Max trukes')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        res['cost_method'] = 'real'
        res['type'] = 'product'
        return res
