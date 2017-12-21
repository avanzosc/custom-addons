# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    almu = fields.Boolean(string='Almu', default=False)
