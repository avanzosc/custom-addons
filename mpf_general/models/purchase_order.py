# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    comunidad_autonoma_nombre = fields.Many2one(
        "x_comunidad_autonoma",
        "Comunidad autónoma",
        related="partner_id.x_studio_comunidad_autnoma",
    )
