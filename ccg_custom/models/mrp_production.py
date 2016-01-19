# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def product_id_change(self, product_id, product_qty):
        res = super(MrpProduction, self).product_id_change(
            product_id=product_id, product_qty=product_qty)
        packaging_obj = self.env['product.packaging']
        product = self.env['product.product'].browse(product_id)
        default_packaging = packaging_obj.search([
            ('is_default', '=', True),
            ('product_tmpl_id', '=', product.product_tmpl_id.id)], limit=1)
        res['value'].update({'product_packaging': default_packaging[:1].id})
        return res

    product_packaging = fields.Many2one(comodel_name='product.packaging',
                                        string='Packaging')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    sale_order_id = fields.Many2one(comodel_name='sale.order',
                                    string='Sale order')
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product template',
        related='product_id.product_tmpl_id')
