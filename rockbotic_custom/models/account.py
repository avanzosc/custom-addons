# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_exempt = fields.Boolean(
        string='Tax exempt', default=False)
