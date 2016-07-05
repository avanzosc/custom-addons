# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_in_sales_order = fields.Boolean('show in sale order', default=False)
