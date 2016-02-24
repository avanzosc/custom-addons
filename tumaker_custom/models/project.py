# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.one
    def _get_project_child_list(self):
        self.project_child_ids = (self.child_ids and
                                  self.search([('analytic_account_id', 'in',
                                                self.child_ids.ids)]).ids or
                                  [])

    project_child_ids = fields.Many2many(comodel_name='project.project',
                                         relation='rel_project_project_child',
                                         column1='parent_id',
                                         column2='project_id',
                                         compute='_get_project_child_list',
                                         string="Project childs")
