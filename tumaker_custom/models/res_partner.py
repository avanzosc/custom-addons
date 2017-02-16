# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('category_id')
    def _compute_partner_category(self):
        for record in self:
            record.partner_category_id = record.category_id[:1]

    partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        compute='_compute_partner_category', store=True)
