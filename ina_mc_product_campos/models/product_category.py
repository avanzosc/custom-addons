# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    stock_seguridad = fields.Float("Stock de Seguridad")
    punto_pedido = fields.Float("Punto de Pedido")
    agrupa_pedido = fields.Integer(
        "Semanas para agrupar Ordenes",
        default=0,
        help="Semanas para agrupar Compras o Fabricacion",
    )
    netea_mps = fields.Boolean(
        string="Netear MPS",
        default=False,
        help="Si se marca Netear MPS, la diferencia entre MPS y ventas del "
        "periodo (semana), se pasan a la siguiente.",
    )
