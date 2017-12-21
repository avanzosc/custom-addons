# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = "product.product"
    _rec_name = 'supercode'

    @api.multi
    @api.depends('default_code', 'name', 'ean13', 'product_tmpl_id.name',
                 'attribute_value_ids', 'attribute_value_ids.name',
                 'customer_ids', 'customer_ids.product_code',
                 'supplier_ids', 'supplier_ids.product_code')
    def _compute_supercode(self):
        ir_trans_obj = self.env['ir.translation']
        for product in self:
            val = []
            for attribute_value in product.attribute_value_ids.filtered(
                    lambda x: x.name):
                val.append(attribute_value.name)
                val.append(ir_trans_obj._get_source(
                    'product.attribute.value,name', 'model', 'es_ES',
                    source=attribute_value.name, res_id=attribute_value.id))
            for supplier in product.supplier_ids.filtered(lambda x:
                                                          x.product_code):
                val.append(supplier.product_code)
            for customer in product.customer_ids.filtered(lambda x:
                                                          x.product_code):
                val.append(customer.product_code)
            if product.default_code:
                val.append(product.default_code)
            if product.name:
                val.append(product.name)
                val.append(ir_trans_obj._get_source(
                    'product.template,name', 'model', 'es_ES',
                    source=product.name, res_id=product.product_tmpl_id.id))
            if product.ean13:
                val.append(product.ean13)
            product.supercode = " ".join(val)

    supercode = fields.Char(string='Supercode', store=True,
                            compute="_compute_supercode")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return models.Model.name_search(self, name=name, args=args,
                                        operator=operator, limit=limit)
