# -*- coding: utf-8 -*-
# © 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    accept_whatsapp = fields.Boolean(
        string='I accept and consent that my telephone number be used to send '
        'me communications whatsapp', default=False)
    accept_center_information = fields.Boolean(
        string='I accept and consent to send information from the center, for '
        'the purpose of commercial prospecting', default=False)
