# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _prepare_mo_vals(self, procurement):
        res = super(ProcurementOrder, self)._prepare_mo_vals(procurement)
        sale_line = procurement.move_dest_id.procurement_id.sale_line_id
        if res:
            res['product_packaging'] = sale_line.product_packaging.id
            res['partner_id'] = sale_line.order_id.partner_id.id
            res['sale_order_id'] = sale_line.order_id.id
        return res
