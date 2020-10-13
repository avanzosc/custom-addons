# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.osv import fields, osv


class purchase_order_line(osv.osv):
    _inherit = "purchase.order.line"

    def _default_date_planned(self, cr, uid, context=None):
        context = context or {}
        if context.get('default_date_planned', False):
            return context.get('default_date_planned')
        return False

    _defaults = {
        'date_planned': _default_date_planned,
    }
