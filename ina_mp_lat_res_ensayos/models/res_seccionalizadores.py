# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResSeccionalizadores(models.Model):
    _name = "res.seccionalizadores"
    _description = "LAT Resultados de ensayo de Seccionalizadores"

    num_serie = fields.Float(string="Numero de Serie", index=True, digits=(15, 0))
    name = fields.Float(string="Numero", digits=(15, 0))
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    version = fields.Char(string="Version SW")
    canal = fields.Integer()
    num_faltas = fields.Integer(string="Num. Faltas")
    corri_faltas = fields.Integer(string="Corriente de Falta")
    tiempo_reset = fields.Integer(string="Tiempo reset")
    retardo = fields.Integer(string="Retardo disparo")
    frecuencia = fields.Integer()
    notas = fields.Char()
    corriente_ok = fields.Boolean(string="Corriente OK")
    disparo_ok = fields.Boolean(string="Disparo OK")
