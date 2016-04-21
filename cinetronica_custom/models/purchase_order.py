# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.multi
    @api.depends('order_id', 'order_id.partner_id', 'product_id',
                 'product_id.seller_ids')
    def compute_sup_ref(self):
        for record in self:
            val = record.product_id.seller_ids.filtered(
                lambda x: x.name.id ==
                record.order_id.partner_id.id).product_code
            record.sup_reference = val

    sup_reference = fields.Char(string="Supplier Reference",
                                compute="compute_sup_ref", store=True)
