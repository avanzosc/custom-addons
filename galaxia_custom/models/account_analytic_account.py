# -*- coding: utf-8 -*-
# © 2016 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api, exceptions, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    agreement_address = fields.Many2one(comodel_name="res.partner")
    recoverable = fields.Selection(
        selection=[('it_recovers', 'It recovers'),
                   ('not_recover', 'He does not recover'),
                   ('is_discounted', 'Is discounted')], string='Recoverable')
    analytic_account_historical_ids = fields.One2many(
        comodel_name='account.analytic.account.historical',
        inverse_name='account_id', string='Account analytic historical')
    recurring_invoice_incidence_ids = fields.One2many(
        string='Recurring invoice incidences',
        comodel_name='account.analytic.recurring.invoice.incidence',
        inverse_name='analytic_account_id')

    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        result = super(
            AccountAnalyticAccount, self.with_context(
                from_automatic_recurring_invoice=True)). _recurring_create_invoice(automatic=automatic)
        return result


class AccountAnalyticRecurringInvoiceIncidence(models.Model):
    _name = 'account.analytic.recurring.invoice.incidence'
    _description = "Recurring invoices incidences"
    _order = "from_date"

    analytic_account_id = fields.Many2one(
        string='Analytic account', comodel_name='account.analytic.account')
    name = fields.Char(string='Description')
    from_date = fields.Date(strin="From date")
    to_date = fields.Date(strin="To date")
    price = fields.Float('Price +/-')


class AccountAnalyticAccountHistorical(models.Model):
    _name = 'account.analytic.account.historical'
    _description = "Account analytic account historical"
    _order = "date"

    account_id = fields.Many2one(
        comodel_name='account.analytic.account', string="Analytic account")
    date = fields.Datetime(strin="Date")
    user_id = fields.Many2one(comodel_name='res.users', string="User")
    name = fields.Char(string="Description")
