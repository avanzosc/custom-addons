# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResInyeccion(models.Model):
    _name = "res.inyeccion"
    _description = "Tabla de resina inyeccion"
    _inherit = ["ina.lat.lot.mixin"]
    _lat_tracking = "lot"

    num_serie = fields.Integer(
        string="Num. Serie Antiguo",
        readonly=True,
        help="Numero de las inyecciones sin producto, que no tienen lote.",
    )
    production_id = fields.Many2one(string="O.F.", comodel_name="mrp.production")
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    fecha = fields.Datetime()
    temp_molde = fields.Integer(string="Temp model (C)")
    pres_inyec = fields.Float(string="Presion inyeccion (bar)", digits=(16, 1))
    pres_curado = fields.Float(string="Presion curado (bar)", digits=(16, 1))
    tim_inyec = fields.Integer(string="Tiempo inyeccion (min)")
    tim_curado = fields.Integer(string="Tiempo curado (min)")
    tim_purga = fields.Integer(string="Tiempo purgado (min)")
    nota = fields.Char(string="Notas")
