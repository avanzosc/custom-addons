# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, _, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    old_reference = fields.Char('Old reference')
    product_moves_ids = fields.One2many('product.move', 'product_id')

    @api.multi
    def write(self, vals):
        if self.old_reference != vals.get('old_reference'):
            body = (_('The reference change from %s to %s') %
                    (self.old_reference, vals.get('old_reference')))
            self.message_post(body=body)
        return super(ProductProduct, self).write(vals)

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        if args is None:
            args = []
        if name:
            ids = self.search(
                cr, user, [('old_reference', operator, name)] + args,
                limit=limit)
            return self.name_get(cr, user, ids, context=context)
        return super(ProductProduct, self).name_search(
            cr, user, name, args=args, operator=operator, context=context,
            limit=limit)
