# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


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
    real_name = fields.Text(
        string='Description', help='This field will contain the description '
        'of the product that will be used in the report')
