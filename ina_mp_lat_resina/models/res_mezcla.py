# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResMezcla(models.Model):
    _name = "res.mezcla"
    _description = "Tabla de resina mezclas"

    production_id4 = fields.Many2one(string="O.F.", comodel_name="mrp.production")
    fecha2 = fields.Datetime(string="Dia de Mezcla")
    peso_comp_a = fields.Float(string="Peso final componente A", digits=(16, 2))
    peso_comp_b = fields.Float(string="Peso final componente B", digits=(16, 2))
    peso_colo = fields.Float(string="Peso colorante", digits=(16, 2))
    peso_filler = fields.Float(string="Peso filler", digits=(16, 2))
    temp_press = fields.Integer(string="Temperatura del pressure pot")
    tim_degas = fields.Integer(string="Tiempo desgasificacion")
    nota4 = fields.Char(string="Notas")
