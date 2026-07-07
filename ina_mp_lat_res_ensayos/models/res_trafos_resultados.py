# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosResultados(models.Model):
    _name = "res.trafos.resultados"
    _description = "LAT Resultados Trafos Resul y Garantias"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie")
    relacion = fields.Char()
    ensayo = fields.Char()
    garantia = fields.Float()
    tolerancia = fields.Char()
    resultado = fields.Float(digits=(9, 2))
    fecha = fields.Datetime()
