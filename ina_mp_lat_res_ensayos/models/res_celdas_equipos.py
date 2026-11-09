# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCeldasEquipos(models.Model):
    _name = "res.celdas.equipos"
    _description = "LAT Resultados de ensayo de Celdas Equipos"
    _inherit = ["ina.lat.lot.mixin"]
    _lat_tracking = "lot"

    celda_id = fields.Many2one(
        string="Ensayo Celdas", comodel_name="res.celdas", ondelete="cascade"
    )
    funcion = fields.Selection(
        [
            ("l1", "L1"),
            ("l2", "L2"),
            ("l3", "L3"),
            ("p1", "P1"),
            ("p2", "P2"),
        ],
    )
    fase = fields.Selection(
        [
            ("r", "R"),
            ("s", "S"),
            ("t", "T"),
        ],
    )
    num_serie = fields.Char(
        string="Num. Serie Antiguo",
        readonly=True,
        help="Numero de serie de los equipos sin producto, que no tienen lote.",
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    nota = fields.Char()
    premo_num = fields.Float(
        string="Num. Premo", digits=(15, 0), related="celda_id.premo_num"
    )
