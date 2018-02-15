# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CrmClaimStage(models.Model):
    _inherit = 'crm.claim.stage'

    closed_stage = fields.Boolean(
        string='Closed Stage',
        help='This fields establishes if a stage is the final stage for a'
             ' claim')
