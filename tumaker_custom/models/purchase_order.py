# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, state='draft'):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name, price_unit=price_unit,
            state=state)
        product_obj = self.env['product.product']
        product = product_obj.browse(product_id)
        analytic_acc = product.expense_analytic_account_id.id or \
            product.categ_id.expense_analytic_account_id.id
        if analytic_acc:
            res['value']['account_analytic_id'] = analytic_acc
        return res
