# -*- coding: utf-8 -*-
# © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models


class ProjectProject(models.Model):
    _inherit = 'project.project'
    _order = 'name'
