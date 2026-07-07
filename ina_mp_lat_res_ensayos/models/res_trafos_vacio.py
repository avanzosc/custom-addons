# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosVacio(models.Model):
    _name = "res.trafos.vacio"
    _description = "LAT Resultados Trafos Vacio"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie")
    devanado = fields.Char()
    tension = fields.Float(string="Tension(V)", digits=(9, 2))
    cor_u = fields.Float(string="Corriente U(A)", digits=(9, 4))
    cor_v = fields.Float(string="Corriente V(A)", digits=(9, 4))
    cor_w = fields.Float(string="Corriente W(A)", digits=(9, 4))
    cor_media1 = fields.Float(string="Corriente Media(A)", digits=(9, 4))
    cor_media2 = fields.Float(string="Corriente Media(%)", digits=(9, 4))
    perdidas = fields.Float(string="Perdidas(W) ", digits=(9, 2))
    fecha = fields.Datetime()
