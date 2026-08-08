# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ComunidadAutonoma(models.Model):
    _name = "x_comunidad_autonoma"
    _description = "Comunidades autónomas"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    x_name = fields.Char("Nombre", required=True, index=True)
    x_active = fields.Boolean("Activo")
    x_studio_sequence = fields.Integer("Secuencia")
