# -*- coding: utf-8 -*-
# © 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def fields_get(self, fields=None, write_access=True):
        group_portal_user = self.env.ref('ds_custom.group_ds_portal_user')
        res = super(ProductProduct, self).fields_get(fields)
        if group_portal_user in self.env.user.groups_id:
            # fields_to_hide = []
            for field in res:
                res[field]['selectable'] = False
        return res
