# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def get_real_code(self, partner_id=False):
        self.ensure_one()
        supinfo_obj = self.env['product.supplierinfo']
        if partner_id:
            customerinfo = supinfo_obj.search(
                [('product_tmpl_id', '=', self.product_tmpl_id.id),
                 ('name', '=', partner_id.id),
                 ('type', '=', 'customer')], limit=1)
            if not customerinfo and partner_id.parent_id:
                customerinfo = supinfo_obj.search(
                    [('product_tmpl_id', '=', self.product_tmpl_id.id),
                     ('name', '=', partner_id.parent_id.id),
                     ('type', '=', 'customer')], limit=1)
            if customerinfo and customerinfo.product_code:
                return customerinfo.product_code
        return self.default_code

    @api.multi
    def get_real_name(self, partner_id=False):
        self.ensure_one()
        supinfo_obj = self.env['product.supplierinfo']
        if partner_id:
            customerinfo = supinfo_obj.search(
                [('product_tmpl_id', '=', self.product_tmpl_id.id),
                 ('name', '=', partner_id.id),
                 ('type', '=', 'customer')], limit=1)
            if not customerinfo and partner_id.parent_id:
                customerinfo = supinfo_obj.search(
                    [('product_tmpl_id', '=', self.product_tmpl_id.id),
                     ('name', '=', partner_id.parent_id.id),
                     ('type', '=', 'customer')], limit=1)
            if customerinfo and customerinfo.product_name:
                return customerinfo.product_name
        return self.name
