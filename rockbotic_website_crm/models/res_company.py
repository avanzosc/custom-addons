# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sepa_responsible = fields.Many2one(
        comodel_name='res.partner', string='Responsible SEPA')
