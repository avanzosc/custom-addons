# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpEnsayos(models.Model):
    _name = "mrp.ensayos"
    _description = "Ensayos LAT"

    name = fields.Char(string="Nombre")
    code = fields.Char(string="Codigo")
