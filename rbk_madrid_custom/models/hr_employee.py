# -*- coding: utf-8 -*-
# Copyright © 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_email = fields.Char(
        string='Work Email', related='address_home_id.email', store=True)
    work_phone = fields.Char(
        string='Work Phone', related='address_home_id.mobile', store=True)
