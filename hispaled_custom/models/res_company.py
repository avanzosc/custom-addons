# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_order_footer = fields.Text(
        string='Sale order footer', translate=True)
    purchase_order_footer = fields.Text(
        string='Purchase order footer', translate=True)
    out_picking_footer = fields.Text(
        string='Out picking footer', translate=True)
    in_picking_footer = fields.Text(
        string='In picking footer', translate=True)
    in_invoice_footer = fields.Text(
        string='In invoice footer', translate=True)
    out_invoice_footer = fields.Text(
        string='Out invoice footer', translate=True)
