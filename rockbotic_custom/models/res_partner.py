# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    magazine = fields.Boolean(string='Magazine', default=False)
    web_blog = fields.Boolean(string='Web/Blog', default=False)
    social_networks = fields.Boolean(string='Social networks', default=False)
    student_rockbotic_level = fields.Char(string='Rockbotic level')
    student_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Students',
        domain=[('active', '=', True), ('registered_partner', '=', True),
                ('employee_id', '=', False)])
    teacher_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Teachers',
        domain=[('active', '=', True), ('registered_partner', '=', True),
                ('employee_id', '!=', False)])
    other_child_ids = fields.One2many(
        comodel_name='res.partner', inverse_name='parent_id',
        string='Contacts',
        domain=[('active', '=', True), ('registered_partner', '=', False)])
