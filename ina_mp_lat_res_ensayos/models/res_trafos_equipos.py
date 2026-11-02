# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosEquipos(models.Model):
    _name = "res.trafos.equipos"
    _description = "LAT Resultados Trafos Equipos"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie Trafo")
    lot_id = fields.Many2one(
        string="Num. Serie Trafo",
        related="trafo_id.lot_id",
        store=True,
    )
    num_serie_equipo = fields.Char(string="Num. Serie Equipo")
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    fecha = fields.Datetime()
    nota = fields.Char()
