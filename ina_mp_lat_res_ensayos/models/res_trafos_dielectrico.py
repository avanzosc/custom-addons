# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafosDielectrico(models.Model):
    _name = "res.trafos.dielectrico"
    _description = "LAT Resultados Trafos Dielectrico"

    trafo_id = fields.Many2one(
        string="Numero Trafo", comodel_name="res.trafos", ondelete="cascade"
    )
    num_serie = fields.Char(string="Num. Serie")
    tipo = fields.Char(string="Tipo Ensayo")
    terminales = fields.Char()
    tension = fields.Integer()
    tiempo = fields.Integer(string="Tiempo(s)")
    frecuencia = fields.Integer(string="Frecuencia(Hz)")
    fecha = fields.Datetime()
