# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPararrayos(models.Model):
    _name = "res.pararrayos"
    _description = "LAT Resultados de ensayo de Pararrayos"

    num_serie = fields.Float(string="Numero de Serie", index=True, digits=(15, 0))
    name = fields.Float(string="Numero", digits=(15, 0))
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(
        string="Producto",
        comodel_name="product.product",
    )
    poten_ensa = fields.Float(string="Potencia Ensayada", digits=(9, 3))
    corri_ensa = fields.Float(string="Corriente Ensayada", digits=(9, 3))
    tensi_refer = fields.Float(string="Tension de referencia", digits=(9, 2))
    riv_ensa = fields.Float(string="Riv Ensayada", digits=(9, 2))
    coro_ensa = fields.Float(string="Corona Ensayada", digits=(9, 2))
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    rechazado = fields.Boolean(default=False)
    orden_conjunto = fields.Many2one(
        string="Orden del Conjunto", comodel_name="mrp.production"
    )
    num_serie_conj = fields.Char(string="Numero de Serie del Conjunto")
    nota = fields.Char(string="Notas")
