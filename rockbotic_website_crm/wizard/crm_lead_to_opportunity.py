# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead2opportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    parent_id = fields.Many2one(
        comodel_name='res.partner', string='Parent',
        domain="[('is_company', '=', True)]")

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(CrmLead2opportunityPartner, self).default_get(fields_list)
        lead_obj = self.env['crm.lead']
        if context.get('active_id'):
            lead = lead_obj.browse(context['active_id'])
            if lead.event_id:
                res.update({'event_id': lead.event_id.id})
            if lead.parent_id:
                res.update({'parent_id': lead.parent_id.id})
        return res
