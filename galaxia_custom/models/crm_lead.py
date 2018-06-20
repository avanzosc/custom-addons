# -*- coding: utf-8 -*-
# Copyright Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    street_2 = fields.Char(
        string='Street', related="partner_id.street")
    street_22 = fields.Char(
        string='Street2', related="partner_id.street2")
    zip2 = fields.Char(
        string='Zip', related="partner_id.zip")
    city2 = fields.Char(
        string='City', related="partner_id.city")
    state2_id = fields.Many2one(
        comodel_name='res.country.state', string='State',
        related='partner_id.state_id')
    country2_id = fields.Many2one(
        comodel_name='res.country', string='Country',
        related='partner_id.country_id')
    zip2_id = fields.Many2one(
        comodel_name='res.better.zip', string='City/Location',
        related='partner_id.zip_id')
