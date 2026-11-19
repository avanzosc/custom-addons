# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class State(models.Model):
    _inherit = "res.country.state"

    x_studio_many2one_field_SUgeq = fields.Many2one(
        "x_comunidad_autonoma", "Comunidad autónoma", index=True, ondelete="restrict"
    )
