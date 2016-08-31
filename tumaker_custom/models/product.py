# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = "product.product"
    _rec_name = 'supercode'

    @api.multi
    @api.depends('default_code', 'name', 'ean13',
                 'attribute_value_ids.name',
                 'customer_ids.product_code',
                 'customer_ids.product_name',
                 'supplier_ids.product_code',
                 'supplier_ids.product_name')
    def _compute_supercode(self):
        for product in self:
            val = []
            for attribute_value in product.attribute_value_ids:
                val.append(attribute_value.name)
            for supplier in product.supplier_ids:
                val += [(supplier.product_code or ''),
                        (supplier.product_name or '')]
            for customer in product.customer_ids:
                val += [(customer.product_code or ''),
                        (customer.product_name or '')]
            if product.default_code:
                val.append(product.default_code)
            if product.name:
                val.append(product.name)
            if product.ean13:
                val.append(product.ean13)
            product.supercode = " ".join(val)

    supercode = fields.Char(string='Supercode', store=True,
                            compute="_compute_supercode")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return models.Model.name_search(self, name=name, args=args,
                                        operator=operator, limit=limit)
