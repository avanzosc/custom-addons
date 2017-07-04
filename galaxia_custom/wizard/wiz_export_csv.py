# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class WizExportCsv(models.TransientModel):
    _name = 'wiz.export.csv'

    csv_file = fields.Binary(string='CSV file', readonly=True)
    csv_fname = fields.Char(string='File name', size=64)
