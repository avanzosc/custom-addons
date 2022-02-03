# -*- coding: utf-8 -*-
# Copyright (c) 2015 Oihane Crucelaegui - AvanzOSC
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    repair_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Repair Analytic Account")
    vat = fields.Char(string="VAT", related='partner_id.vat', readonly=True)
    date_order = fields.Datetime(default=False)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({'date_order': fields.Date.context_today(self)})
        return super(PurchaseOrder, self).copy(default)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    repair_id = fields.Many2one(
        comodel_name='mrp.repair', string="Repair Order")

    @api.model
    def create(self, vals):
        line = super(PurchaseOrderLine, self).create(vals)
        if line.order_id:
            lines = line.order_id.order_line.filtered(lambda x: x.repair_id)
            for line in lines:
                if line.repair_id.state in ('done', '2binvoiced', 'cancel'):
                    raise exceptions.Warning(
                        _('You cannot add lines to this purchase order. '
                          'The purchase lines with product: %s, is associated '
                          'with the repair order: %s, and its status is '
                          'completed, or to be invoiced.') %
                        (line.name, line.repair_id.name))
        return line
