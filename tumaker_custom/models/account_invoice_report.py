# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Partner category', readonly=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
            ", sub.partner_category_id as partner_category_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + \
            ", partner.partner_category_id as partner_category_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + \
            ", partner.partner_category_id"
