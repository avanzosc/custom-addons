# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    fichar = fields.Selection(
        selection=[
            ("no", "No Ficha"),
            ("oficina", "Oficina/Almacen"),
            ("fabrica", "Fabrica"),
        ],
        string="Fichar en",
        default="fabrica",
    )
