# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, SUPERUSER_ID


def update_last_purchase_info(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        purchase_lines = env['purchase.order.line'].search(
            [('state', 'in', ['confirmed', 'done'])])
        for product in purchase_lines.mapped('product_id'):
            product._get_last_purchase()


def migrate(cr, version):
    if not version:
        return
    update_last_purchase_info(cr)
