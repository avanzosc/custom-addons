# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fecha_confirmada = fields.Datetime(
        "Fecha Planificada",
        tracking=True,
        default=lambda self: fields.Date.context_today(self),
    )
