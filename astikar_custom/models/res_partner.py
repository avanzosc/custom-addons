# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_company = fields.Boolean(default=True)
    campaign_id = fields.Many2one(
        comodel_name='crm.tracking.campaign', string="Campaign")
    medium_id = fields.Many2one(
        comodel_name='crm.tracking.medium', string="Channel")
    source_id = fields.Many2one(comodel_name='crm.tracking.source',
                                string='Source')
