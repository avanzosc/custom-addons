# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_registry = fields.Char(size=128)
