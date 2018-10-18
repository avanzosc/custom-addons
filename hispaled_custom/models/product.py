# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_luminclase_image(self):
        self.ensure_one()
        att_clase = self.env['product.attribute'].search(
            [('attribute_code', '=', 'LUM-CLA')])
        clase_value = self.attribute_value_ids.filtered(
            lambda a: a.attribute_id == att_clase[:1])
        if clase_value[:1].name == u'I':
            return 1
        elif clase_value[:1].name == u'II':
            return 2
        elif clase_value[:1].name == u'III':
            return 3
        return False


class ProductConfiguratorAttribute(models.Model):
    _inherit = 'product.configurator.attribute'
    _order = 'attribute_code'

    attribute_code = fields.Char(
        string='Attribute Code', related='attribute_id.attribute_code',
        store=True)


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _order = 'attribute_code'
