# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    old_reference = fields.Char(string='Old reference')
    product_moves_ids = fields.One2many(
        comodel_name='product.move', inverse_name='product_id',
        string='Product Moves')

    @api.multi
    def write(self, vals):
        if ('old_reference' in vals and
                self.old_reference != vals.get('old_reference')):
            body = (
                _('The reference change from %s to %s') %
                (self.old_reference or "''",
                 vals.get('old_reference') or "''"))
            self.message_post(body=body)
        return super(ProductProduct, self).write(vals)

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        if args is None:
            args = []
        products = super(ProductProduct, self).name_search(
            cr, user, name=name, args=args, operator=operator, context=context,
            limit=limit)
        ids = [x[0] for x in products]
        if name:
            ids = self.search(cr, user,
                              ['|', ('id', 'in', ids),
                               ('old_reference', operator, name)],
                              limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
