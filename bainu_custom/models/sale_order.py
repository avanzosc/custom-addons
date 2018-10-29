# -*- coding: utf-8 -*-
# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_opportunity(self):
        crm_obj = self.env['crm.lead']
        lead = crm_obj.search([('ref', '=', u'sale.order,{}'.format(self.id))])
        if lead:
            lead.stage_id = self.env.ref('crm.stage_lead6')

    @api.multi
    def action_button_confirm(self):
        self.update_opportunity()
        return super(SaleOrder, self).action_button_confirm()
