# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ampa_partner = fields.Boolean(string='AMPA partner', default=False)
