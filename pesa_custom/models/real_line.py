# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class RealLine(models.Model):
    _name = 'real.line'

    def _default_company(self):
        return self.env.user.company_id

    name = fields.Char(string='Name')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 default=_default_company)
