# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit='project.task.type'

    task_phase=fields.Many2one(comodel_name='task.phase', string='Task '
                                                                   'Phase')

    #anak nahi du many2many bat partner(otros clientesea)
    partner_ids=fields.Many2many(comodel_name='res.partner',
                                   string='Attendances')
    
    user_id=fields.Many2one(comodel_name='res.user',
                               string='Responsible')
    


class TaskPhase(models.Model):
    _name='task.phase'

    name=fields.Char(string='name')
    description=fields.Char(string='description')
