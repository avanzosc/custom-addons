# -*- coding: utf-8 -*-
# © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.osv import fields, osv


class stock_move(osv.osv):
    _inherit = "stock.move"

    def _default_date(self, cr, uid, context=None):
        context = context or {}
        if context.get('default_picking_type_id', False):
            pick_type = self.pool.get(
                'stock.picking.type').browse(
                cr, uid, context['default_picking_type_id'], context=context)
            if pick_type.code != 'incoming':
                return fields.datetime.now()
            else:
                if context.get('default_date', False):
                    return context.get('default_date')
        return fields.datetime.now()

    def _default_date_expected(self, cr, uid, context=None):
        context = context or {}
        if context.get('default_picking_type_id', False):
            pick_type = self.pool.get(
                'stock.picking.type').browse(
                cr, uid, context['default_picking_type_id'], context=context)
            if pick_type.code != 'incoming':
                return fields.datetime.now()
            else:
                if context.get('default_date_expected', False):
                    return context.get('default_date_expected')
        return fields.datetime.now()

    _defaults = {
        'date': _default_date,
        'date_expected': _default_date_expected,
    }
