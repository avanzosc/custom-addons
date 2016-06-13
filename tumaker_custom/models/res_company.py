# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    rml_footer = fields.Text(translate=True)
