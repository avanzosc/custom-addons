# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    falta_material = fields.Boolean(default=False)
    refer_falta_material = fields.Text("Referencias que Faltan")
    aceptada = fields.Float("Cant. Aceptada", digits=(9, 2))
    rechazada = fields.Float("Cant. Rechazada", digits=(9, 2))
