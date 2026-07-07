# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosRelacion(models.Model):
    _name = "res.trafos.relacion"
    _description = "LAT Resultados Trafos relacion"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie")
    at_bt = fields.Char(string="AT/BT")
    posicion = fields.Integer()
    conexion = fields.Integer()
    val_teori = fields.Float(string="Valor teorico", digits=(9, 2))
    fase_u = fields.Float(digits=(9, 3))
    fase_v = fields.Float(digits=(9, 3))
    fase_w = fields.Float(digits=(9, 3))
    simbol_acopla = fields.Char(string="Simbolo acoplamiento")
    fecha = fields.Datetime()
