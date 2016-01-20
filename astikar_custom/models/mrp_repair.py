# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    def _defaul_quotation_notes(self):
        return self.env.user.company_id.sale_note

    name = fields.Char(default='/')
    quotation_notes = fields.Text(default=_defaul_quotation_notes)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).copy(default)
