# -*- coding: utf-8 -*-
# Copyright (c) 2016 Esther Martín - AvanzOSC
# Copyright (c) 2019 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    campaign_id = fields.Many2one(
        comodel_name='crm.tracking.campaign', string="Campaign")
    medium_id = fields.Many2one(
        comodel_name='crm.tracking.medium', string="Channel")
    source_id = fields.Many2one(comodel_name='crm.tracking.source',
                                string='Source')

    @api.multi
    @api.onchange('vat')
    def vat_change(self, value):
        res = super(ResPartner, self).vat_change(value=value)
        if value:
            result = self.search([('vat', '=', value), ])
            if result:
                res.update({
                    'warning': {
                        'title': _('Info'),
                        'message': _('VAT already exist: {}').format((value)),
                        },
                })
        return res
