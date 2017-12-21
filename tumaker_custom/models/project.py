# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def _compute_project_child_list(self):
        for record in self:
            record.project_child_ids = (
                record.child_ids and record.search(
                    [('analytic_account_id', 'in', record.child_ids.ids)]
                ).ids or [])

    project_child_ids = fields.Many2many(comodel_name='project.project',
                                         relation='rel_project_project_child',
                                         column1='parent_id',
                                         column2='project_id',
                                         compute='_compute_project_child_list',
                                         string="Project childs")
