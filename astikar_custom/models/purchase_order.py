# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    repair_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string="Repair Analytic Account")
