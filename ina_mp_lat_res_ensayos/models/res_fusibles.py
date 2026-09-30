# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResFusibles(models.Model):
    _name = "res.fusibles"
    _description = "LAT Resultados de ensayo de Fusibles"
    _inherit = ["ina.lat.lot.mixin"]

    name = fields.Char(string="Numero")
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(
        string="Producto",
        comodel_name="product.product",
    )
    product_name = fields.Char(string="Descripcion")
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    res_nominal = fields.Float(string="Res. Nominal", digits=(9, 3))
    tol_resis = fields.Float(string="Tol. Resis", digits=(9, 3))
    res_medida = fields.Float(string="Res. Medida", digits=(9, 3))
    peso_nominal = fields.Float(digits=(9, 3))
    tol_peso = fields.Float(string="Tol. Peso", digits=(9, 3))
    peso_medido = fields.Float(digits=(9, 3))
    rechazado_resis = fields.Boolean(string="Rechazado Resistencia", default=False)
    rechazado_peso = fields.Boolean(default=False)
