# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re
from openerp import models
from openerp.models import expression
from openerp.tools.safe_eval import safe_eval as eval


class ProductProduct(models.Model):

    _inherit = "product.product"

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            ids = []
            if operator in positive_operators:
                ids = self.search(cr, user, [('default_code', '=', name)] +
                                  args, limit=limit, context=context)
                if not ids:
                    ids = self.search(
                        cr, user, [('ean13', '=', name)] + args, limit=limit,
                        context=context)
            if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args +
                                  [('default_code', operator, name)],
                                  limit=limit, context=context)
                if not limit or len(ids) < limit:
                    limit2 = (limit - len(ids)) if limit else False
                    ids += self.search(
                        cr, user, args + [('name', operator, name),
                                          ('id', 'not in', ids)],
                        limit=limit2, context=context)
                    ids += self.search(
                        cr, user, args +
                        [('attribute_value_ids.name', operator, name),
                         ('id', 'not in', ids)], limit=limit2, context=context)
            elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(
                    cr, user, args + ['&', ('default_code', operator, name),
                                      ('name', operator, name)], limit=limit,
                    context=context)
                remove_ids = []
                for record in self.browse(cr, user, ids, context=context):
                    for line in record.attribute_value_ids:
                        if not eval('"'+str(line.name) + '" ' + operator +
                                    ' "' + str(name) + '"'):
                            remove_ids.append(record.id)
                for record in remove_ids:
                    ids.remove(record)
            if not ids and operator in positive_operators:
                ptrn = re.compile(r'(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(
                        cr, user, [('default_code', '=', res.group(2))] + args,
                        limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result
