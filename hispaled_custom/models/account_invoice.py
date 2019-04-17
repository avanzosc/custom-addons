# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_order_id = fields.Many2one(
        string='Sale order', comodel_name='sale.order')
    client_order_ref = fields.Char(
        string='Sale order Reference/Description', store=True,
        related='sale_order_id.client_order_ref')
    project_id = fields.Many2one(
        string='Project', comodel_name='account.analytic.account',
        related='sale_order_id.project_id', store=True)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        product_obj = self.env['product.product']
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        if product:
            prod = product_obj.browse(product)
            if self.env.context.get('type', False) == 'out_invoice':
                new_value = product_obj.onchange_product_id_hispaled(
                    product_id=product)
                value = res.setdefault('value', {})
                value.update(new_value)
                if prod.description_sale:
                    value['name'] += '\n' + prod.description_sale
            if self.env.context.get('type', False) == 'in_invoice':
                name = prod.name_template
                if prod.variant_description:
                    name += '\n' + prod.variant_description
                    res['value']['name'] = name
        return res
