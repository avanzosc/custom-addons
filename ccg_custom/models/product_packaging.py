# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    is_default = fields.Boolean(string='Default', default=False)
