# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class CrmLeadEventPick(models.TransientModel):
    _inherit = "crm.lead.event.pick"

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(CrmLeadEventPick, self).default_get(fields_list)
        if 'active_id' in context:
            lead = self.env[context.get('active_model')].browse(context.get(
                'active_id'))
            res.update({'event_id': lead.event_id.id})
        return res
