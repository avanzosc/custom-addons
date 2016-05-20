# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

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
