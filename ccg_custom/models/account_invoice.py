# -*- coding: utf-8 -*-
# Copyright (c) 2018  Daniel Campos - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    discounted = fields.Boolean(string="Discounted")
