# -*- coding: utf-8 -*-
# (c) 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_registry = fields.Char(size=196)
    vat_exempt_note = fields.Text()
