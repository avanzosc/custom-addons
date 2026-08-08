# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    aceptada = fields.Float("Cant. Aceptada", digits=(9, 2))
    rechazada = fields.Float("Cant. Rechazada", digits=(9, 2))
    falta_material = fields.Boolean(default=False)
    estado = fields.Selection(
        selection=[
            ("activa", "Activa"),
            ("interrumpida", "Interrumpida"),
            ("procesada", "Procesada"),
            ("cancelada", "Cancelada"),
        ],
    )
