# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaimResponsible(models.Model):
    _name = 'crm.claim.responsible'
    _description = 'Claim responsible'

    name = fields.Char()


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    @api.depends('date_action_next', 'date_deadline')
    def _compute_calendar_date(self):
        for claim in self:
            claim.calendar_date = claim.date_action_next or claim.date_deadline

    @api.multi
    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            return {'domain': {
                    'real_line_id': [('company_id', '=', self.company_id.id)],
                    'journey_id': [('company_id', '=', self.company_id.id)],
                    'schedule_id': [('company_id', '=', self.company_id.id)],
                    }}

    @api.multi
    @api.depends('from_related_claims', 'to_related_claims')
    def _compute_priority(self):
        if self.from_related_claims:
            self.priority = '4'
        else:
            self.priority = '1'

    line = fields.Char(string='Line')
    real_line_id = fields.Many2one(comodel_name='real.line',
                                   string='Real line')
    journey_id = fields.Many2one(comodel_name='journey',
                                 string='Journey')
    schedule_id = fields.Many2one(comodel_name='schedule', string='Schedule')
    driver_id = fields.Many2one(comodel_name='res.users', string='Driver')
    book_number = fields.Integer(string='Book number')
    book_page = fields.Integer(string='Book page')
    service_date = fields.Date(string='Service date')
    calendar_date = fields.Date(compute='_compute_calendar_date', store=True)
    priority = fields.Selection([('0', 'Lowest'), ('1', 'Low'),
                                 ('2', 'Normal'), ('3', 'High'),
                                 ('4', 'Highest')], string='Priority',
                                compute='_compute_priority', store=True)
    claim_responsible_id = fields.Many2one(
        comodel_name='crm.claim.responsible', string='Claim responsible')
