# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResSeccionadores(models.Model):
    _name = "res.seccionadores"
    _description = "LAT Resultados de ensayo de Seccionadores"

    name = fields.Char(string="Numero")
    num_serie = fields.Char(string="Numero de Serie", index=True)
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    product_name = fields.Char(string="Descripcion")
    fecha_ensayo = fields.Datetime(default=fields.Datetime.now)
    ensayo_calidad = fields.Boolean(default=False)
    unipolar = fields.Boolean(default=False)
    res_nominal = fields.Float(string="Res. Nominal", digit=(9, 3))
    tol_resis = fields.Float(string="Tol. Resis", digit=(9, 3))
    res_r_medida = fields.Float(string="Res. r Medida", digit=(9, 3))
    res_s_medida = fields.Float(string="Res. s Medida", digit=(9, 3))
    res_t_medida = fields.Float(string="Res. t Medida", digit=(9, 3))
    ensayo_finalizado = fields.Boolean(default=False)
