# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


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

    @api.multi
    def onchange_product_id_hispaled(self, product_id):

        res = {}
        if product_id:
            product = self.env['product.product'].browse(product_id)
            attr_values_dict = product._get_product_attributes_values_dict()
            for val in attr_values_dict:
                val['product_tmpl_id'] = product.product_tmpl_id.id
                val['owner_model'] = self._name
                val['owner_id'] = self.id
            res['name'] = self._get_product_description_hispaled(
                product.product_tmpl_id, product,
                product.attribute_value_ids)
        return res

    @api.model
    def _order_attributes_hispaled(self, template, product_attribute_values):
        res = template._get_product_attributes_dict()
        res2 = []
        for val in res:
            value = product_attribute_values.filtered(
                lambda x: x.attribute_id.id == val['attribute_id'])
            if value:
                val['value_id'] = value
                res2.append(val)
        return res2

    @api.model
    def _get_product_description_hispaled(self, template, product,
                                          product_attributes):
        name = product and product.name or template.name
        extended = self.user_has_groups(
            'product_variants_no_automatic_creation.'
            'group_product_variant_extended_description')
        if not product_attributes and product:
            product_attributes = product.attribute_value_ids
        values = self._order_attributes_hispaled(template, product_attributes)
        if extended:
            description = "\n".join(
                "%s: %s" %
                (x['value_id'].attribute_id.name, x['value_id'].name)
                for x in values)
        else:
            description = ", ".join([x['value_id'].name for x in values])
        if not description:
            return name
        return ("%s\n%s" if extended else "%s (%s)") % (name, description)


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _order = 'sequence, name asc'


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'
    _order = 'sequence asc'

    sequence = fields.Integer(
        string='Sequence', related='attribute_id.sequence', store=True)


class ProductConfiguratorAttribute(models.Model):
    _inherit = 'product.configurator.attribute'
    _order = 'attribute_sequence'

    attribute_sequence = fields.Integer(
        string='Sequence', related='attribute_id.sequence', store=True)
