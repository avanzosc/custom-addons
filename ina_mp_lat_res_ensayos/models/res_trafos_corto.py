# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosCorto(models.Model):
    _name = "res.trafos.corto"
    _description = "LAT Resultados Trafos Corto"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie")
    relacion = fields.Char()
    posicion = fields.Integer()
    tension = fields.Float(string="Tension(V)", digits=(9, 2))
    cor_u = fields.Float(string="Corriente U(A)", digits=(9, 4))
    cor_v = fields.Float(string="Corriente V(A)", digits=(9, 4))
    cor_w = fields.Float(string="Corriente W(A)", digits=(9, 4))
    cor_media1 = fields.Float(string="Corriente Media(A)", digits=(9, 4))
    perdidas = fields.Float(string="Perdidas(W) ", digits=(9, 2))
    temperatura = fields.Float()
    fecha = fields.Datetime()
