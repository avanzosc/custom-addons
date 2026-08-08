# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # *************************************************************************
    # ¡! OJO
    # * Campos x_studio se deben mantener exactamente igual a cómo los creó el
    # * cliente con Studio para evitar pérdidas o duplicidades de datos
    # *******************************************************************************
    x_studio_comunidad_autnoma = fields.Many2one(
        "x_comunidad_autonoma",
        "Comunidad autónoma",
        related="state_id.x_studio_many2one_field_SUgeq",
    )
