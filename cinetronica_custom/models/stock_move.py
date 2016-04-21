# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    @api.depends('picking_id', 'picking_id.partner_id', 'product_id',
                 'product_id.seller_ids')
    def compute_sup_ref(self):
        for record in self:
            val = ''
            if (record.picking_id and
                    (record.location_id.usage == 'supplier' or
                     record.location_dest_id.usage == 'supplier') and
                    record.product_id):
                partners = [
                    record.picking_id.partner_id.id,
                    record.picking_id.partner_id.commercial_partner_id.id]
                val = record.product_id.seller_ids.filtered(
                    lambda x: x.name.id in partners).product_code
            record.sup_reference = val

    sup_reference = fields.Char(string="Supplier Reference",
                                compute="compute_sup_ref", store=True)
