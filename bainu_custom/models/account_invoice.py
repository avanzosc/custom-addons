# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api
from lxml import etree


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    almu = fields.Boolean(string='Almu', default=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        user_obj = self.env['res.users']
        low = user_obj.has_group('bainu_custom.group_account_viewer')
        high = user_obj.has_group('account.group_account_invoice')
        if low and not high:
            root = etree.fromstring(res['arch'])
            root.set('create', 'false')
            root.set('edit', 'false')
            res['arch'] = etree.tostring(root)
        return res
