# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    city = fields.Char(
        'Town', related='partner_shipping_id.city', store=True)
    street2 = fields.Char(
        'District', related="partner_shipping_id.street2", store=True)
    registration_note = fields.Text()
    no_pa_price = fields.Float(
        string='No PA price', help='Price for those partners that do not '
        'belong to the Parents Association')
    print_sum = fields.Boolean(default=False)

    @api.multi
    def _prepare_recurring_invoice_lines(self, line):
        vals = super(SaleOrder, self)._prepare_recurring_invoice_lines(line)
        vals['name'] = line.group_description
        return vals

    @api.multi
    def copy(self, default=None):
        new_order = super(SaleOrder, self).copy(default)
        lines = new_order.mapped('order_line').filtered(
            lambda x: x.group_description and self.name in x.group_description)
        for line in lines:
            line.group_description = (
                line.group_description.replace(self.name, line.order_id.name))
        return new_order


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    apply_performance = fields.Boolean(default=False)
    apply_performance_by_quantity = fields.Boolean(default=False)
    week1 = fields.Boolean(default=True)
    week2 = fields.Boolean(default=True)
    week3 = fields.Boolean(default=True)
    week4 = fields.Boolean(default=True)
    week5 = fields.Boolean(default=True)
    week6 = fields.Boolean(default=True)
    real_name = fields.Html(
        string='Description', help='This field will contain the description '
        'of the product that will be used in the report')
    group_description = fields.Char(copy=True)
    courses = fields.Char(copy=True)
