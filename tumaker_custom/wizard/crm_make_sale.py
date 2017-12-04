# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class CrmMakeSale(models.TransientModel):

    _inherit = "crm.make.sale"

    warehouse_id = fields.Many2one(comodel_name='stock.warehouse',
                                   required=True,
                                   string="Warehouse")

    @api.multi
    def makeOrder(self):
        return super(CrmMakeSale,
                     self.with_context(force_warehouse=self.warehouse_id.id)
                     ).makeOrder()


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        force_warehouse = self.env.context.get('force_warehouse', False)
        if force_warehouse:
            values.update({'warehouse_id': force_warehouse})
        return super(SaleOrder, self).create(values)
