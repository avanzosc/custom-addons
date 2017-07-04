# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons.event_track_assistant._common import\
    _convert_to_local_date


class ProjectProject(models.Model):
    _inherit = 'project.project'
    _order = 'name'


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    @api.multi
    @api.depends('project', 'project.user_id', 'project.members')
    def _compute_project_info(self):
        for i in self.filtered(lambda x: x.project):
            i.project_manager_id = i.project.user_id
            i.project_members_ids = [(6, 0, i.project.members.ids)]

    @api.depends('date')
    def _compute_session_date(self):
        for work in self.filtered('date'):
            from_date = _convert_to_local_date(work.date, self.env.user.tz)
            work.day = str(from_date.date().weekday())

    project_manager_id = fields.Many2one(
        comodel_name='res.users', string='Project manager',
        compute='_compute_project_info', store=True)
    project_members_ids = fields.Many2many(
        comodel_name='res.users', string='Project members',
        compute='_compute_project_info', store=True)
    user_id = fields.Many2one(
        comodel_name='res.users', default=False)
    day = fields.Selection(
        selection=[('0', 'Monday'),
                   ('1', 'Tuesday'),
                   ('2', 'Wednesday'),
                   ('3', 'Thursday'),
                   ('4', 'Friday'),
                   ('5', 'Saturday'),
                   ('6', 'Sunday')],
        string='Day of the week', compute='_compute_session_date', store=True)
