# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    key_code = fields.Char()
    presence_ids = fields.One2many(
        string='Presences', comodel_name='event.track.presence',
        inverse_name='event')
    recurring_invoice_line_ids = fields.One2many(
        string='Invoice Lines', comodel_name='account.analytic.invoice.line',
        related='analytic_account_id.recurring_invoice_line_ids')
    recurring_invoice_incidence_ids = fields.One2many(
        string='Recurring invoice incidences',
        comodel_name='account.analytic.recurring.invoice.incidence',
        related='analytic_account_id.recurring_invoice_incidence_ids')


class EventTrackPresence(models.Model):
    _inherit = 'event.track.presence'

    recoverable = fields.Selection(
        selection=[('it_recovers', 'It recovers'),
                   ('not_recover', 'He does not recover'),
                   ('is_discounted', 'Is discounted')],
        related='event.sale_order.project_id.recoverable', store=True,
        string='Recoverable')
    task_id = fields.Many2one(
        comodel_name="project.task", related="session.task_id", store=True,
        string='Task')

    @api.depends('session', 'session.allowed_partner_ids')
    def _compute_allowed_partner_ids(self):
        all_partners = self.env['marketing.config.settings']._get_parameter(
            'show.all.customers.in.presences')
        if all_partners and all_partners.value == 'True':
            cond = [('employee_id', '!=', False)]
            partners = self.env['res.partner'].search(cond)
        for presence in self:
            list = presence.session.allowed_partner_ids.ids
            if all_partners and all_partners.value == 'True':
                list += partners.ids
            presence.allowed_partner_ids = [(6, 0, list)]
