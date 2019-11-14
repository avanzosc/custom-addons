# -*- coding: utf-8 -*-
# Copyright (c) 2015 Oihane Crucelaegui - AvanzOSC
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    repair_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Repair Analytic Account")
    vat = fields.Char(string="VAT", related='partner_id.vat', readonly=True)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    repair_id = fields.Many2one(
        comodel_name='mrp.repair', string="Repair Order")
