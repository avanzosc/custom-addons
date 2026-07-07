# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCeldasSeccionadores(models.Model):
    _name = "res.celdas.seccionadores"
    _description = "LAT Resultados de ensayo de Celdas Seccionadores"

    celda_id = fields.Many2one(
        string="Ensayo Celdas", comodel_name="res.celdas", ondelete="cascade"
    )
    #   product_id =fields.Many2one("product.product", string="Producto" )
    num_maniobras = fields.Integer(string="Num. Maniobras")
    resis_nomi = fields.Float(string="Res. Nominal", digits=(8, 2))
    tol_resis = fields.Float(string="Tol. Res", digits=(8, 2))
    res_r_med = fields.Float(string="Res r Med", digits=(8, 2))
    res_s_med = fields.Float(string="Res s Med", digits=(8, 2))
    res_t_med = fields.Float(string="Res t Med", digits=(8, 2))
    vel_nom_aper = fields.Float(string="Vel. nom. Aper", digits=(8, 2))
    tol_vel_aper = fields.Float(string="Tol. vel. Aper", digits=(8, 2))
    vel_aper_med = fields.Float(string="Vel. Aper Med", digits=(8, 2))
    vel_nom_cier = fields.Float(string="Vel. nom. Cierre", digits=(8, 2))
    tol_vel_cier = fields.Float(string="Tol. vel. Cierre", digits=(8, 2))
    vel_cier_med = fields.Float(string="Vel. Cierre Med", digits=(8, 2))
    tiempo_fases_max = fields.Float(string="Tiempo fases Max", digits=(8, 2))
    tiempo_aper_med = fields.Float(string="Tiempo aper  Med", digits=(8, 2))
    tiempo_cierre_med = fields.Float(digits=(8, 2))
    fecha_res_vel = fields.Datetime()
    ens_res_vel = fields.Boolean(string="Ensayo Res Vel", default=False)
    ensayo_resis = fields.Boolean(string="Ensayado Resist", default=False)
    ensayo_veloc = fields.Boolean(string="Ensayado Veloc.", default=False)
    premo_num = fields.Float(string="Num. Premo", digits=(15, 0))
    posicion = fields.Integer()
    seccionador = fields.Char()
    descripcion = fields.Char()
