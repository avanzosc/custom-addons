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

    @api.multi
    @api.depends('quant_ids', 'quant_ids.location_id',
                 'quant_ids.location_id.usage', 'quant_ids.qty')
    def _compute_real_stock(self):
        for record in self:
            record.real_stock = sum(
                record.quant_ids.filtered(lambda x: x.location_id.usage ==
                                          'internal').mapped('qty'))

    @api.multi
    @api.depends('move_ids', 'move_ids.state')
    def _compute_count_move_ids(self):
        for record in self:
            record.count_move_ids = len(record.move_ids.filtered(
                lambda x: x.state == 'done'))

    real_stock = fields.Float(string="Real Stock",
                              compute="_compute_real_stock", store=True)
    supercode = fields.Char(string='Supercode', store=True,
                            compute="_compute_supercode")
    quant_ids = fields.One2many(comodel_name="stock.quant",
                                inverse_name="product_id", string="Quants")
    move_ids = fields.One2many(comodel_name="stock.move",
                               inverse_name="product_id", string="Moves")
    count_move_ids = fields.Integer(
        string="Move Count", compute="_compute_count_move_ids", store=True)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return models.Model.name_search(self, name=name, args=args,
                                        operator=operator, limit=limit)

    def _search(self, cr, user, args, offset=0, limit=None, order=None,
                context=None, count=False, access_rights_uid=None):
        order_by = context.get('order_by', False)
        if order_by:
            order = order_by
        return super(ProductProduct, self)._search(
            cr, user, args, offset=offset, limit=limit, order=order,
            context=context, count=count, access_rights_uid=access_rights_uid)
