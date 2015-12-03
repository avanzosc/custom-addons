# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class Machinery(models.Model):
    _inherit = 'machinery'

    sale_cost = fields.Float('Sale Value', digits=(16, 2))
