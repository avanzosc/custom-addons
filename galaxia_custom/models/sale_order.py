# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_services_amounts(self):
        for sale in self:
            cur = sale.pricelist_id.currency_id
            total = 0.00
            taxes = 0.00
            for line in sale.service_order_line:
                total += line.monthly_amount
                for c in line.tax_id.compute_all(
                        1.00, line.monthly_amount, line.product_id,
                        line.order_id.partner_id)['taxes']:
                    taxes += c.get('amount', 0.0)
            sale.services_amount_untaxed = cur.round(total)
            sale.services_amount_tax = cur.round(taxes)
            sale.services_amount_total = (
                sale.services_amount_untaxed + sale.services_amount_tax)

    amount_untaxed = fields.Float(
        string='Untaxed Amount', digits=dp.get_precision('Precision in sales'))
    amount_tax = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))
    amount_total = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))
    services_amount_untaxed = fields.Float(
        string='Services untaxed amount',
        digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')
    services_amount_tax = fields.Float(
        string='Services taxes', digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')
    services_amount_total = fields.Float(
        string='Services amount total',
        digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')

    @api.multi
    def action_button_confirm(self):
        return super(SaleOrder, self.with_context(
            without_sale_name=True)).action_button_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_id', 'product_tmpl_id')
    def _compute_product_type(self):
        super(SaleOrderLine, self)._compute_product_type()
        for line in self:
            if not line.product_type and line.product_tmpl_id:
                line.product_type = line.product_tmpl_id.type

    def _compute_service_time(self):
        for line in self:
            seconds = line.weekly_hours * 3600
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            line.service_time = "%d:%02d:%02d" % (h, m, s)

    apply_performance = fields.Boolean(default=False)
    price_unit = fields.Float(
        string='Unit Price', digits=dp.get_precision('Precision in sales'))
    price_subtotal = fields.Float(
        string='Subtotal', digits=dp.get_precision('Precision in sales'))
    periodicity = fields.Char(string='Periodicity')
    service_time = fields.Char(
        string='Service time', compute='_compute_service_time')
