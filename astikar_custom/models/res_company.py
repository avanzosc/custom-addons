# -*- coding: utf-8 -*-
# Copyright (c) 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    lopd_eusk_text = fields.Text(string="LOPD for Basque reports")
    lopd_cast_text = fields.Text(string="LOPD for Spanish reports")
    general_conditions = fields.Html(
        string="General conditions in Basque")
    general_conditions_cas = fields.Html(
        string="General conditions in Spanish")
    sale_note = fields.Html(
        string="'Default Terms and Conditions", translate=True,
        help="Default terms and conditions for quotations.")
