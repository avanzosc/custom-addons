# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.depends('repair_ids')
    def _compute_has_repairs(self):
        for invoice in self:
            invoice.has_repairs = bool(invoice.repair_ids)

    repair_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Repair Analytic Account")
    repair_ids = fields.One2many(
        comodel_name='mrp.repair', inverse_name='invoice_id',
        string='Repair order')
    has_repairs = fields.Boolean(compute='_compute_has_repairs',
                                 string='Has repairs')
    warning = fields.Text(string='Warning')
    not_warning = fields.Boolean(string='Hide Warning Message', default=True)

    @api.model
    def create(self, vals):
        if vals.get('partner_id', False):
            part = self.env['res.partner'].browse(vals.get('partner_id'))
            if part.invoice_warn:
                vals.update({'not_warning': False,
                             'warning': part.invoice_warn_msg})
        return super(AccountInvoice, self).create(vals)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    date_invoice = fields.Date(string="Invoice date",
                               related="invoice_id.date_invoice",
                               store=True, readonly=True)

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        if ('account_analytic_id' in res['value'] and not
                res['value'].get('account_analytic_id', False)):
            res['value'].pop('account_analytic_id')
        return res
