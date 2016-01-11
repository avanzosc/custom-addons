# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def _default_product_packaging(self):
        packaging_obj = self.env['product.packaging']
        default_packaging = packaging_obj.search([('is_default', '=', True)])
        return default_packaging and default_packaging[:1].id

    product_packaging = fields.Many2one(comodel_name='product.packaging',
                                        string='Packaging',
                                        default=_default_product_packaging)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    sale_order_id = fields.Many2one(comodel_name='sale.order',
                                    string='Sale order')
