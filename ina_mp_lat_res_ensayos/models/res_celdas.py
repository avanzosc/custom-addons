# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCeldas(models.Model):
    _name = "res.celdas"
    _description = "LAT Resultados de ensayo de Celdas"

    name = fields.Float(string="Numero", digits=(15, 0))
    venta_id = fields.Many2one(string="Orden Venta", comodel_name="sale.order")
    premo_num = fields.Float(string="Num. Premo", digits=(15, 0))
    premo_ref = fields.Many2one(string="Ref. Premo", comodel_name="product.product")
    premo_fecha = fields.Datetime(string="Fecha Premo")
    mont_num = fields.Float(string="Num. Montaje", digits=(15, 0))
    mont_ref = fields.Many2one(string="Ref. Montaje", comodel_name="product.product")
    mont_fecha = fields.Datetime(string="Fecha Montaje")
    llenado_num = fields.Float(string="Num. Llenado", digits=(15, 0))
    llenado_ref = fields.Many2one(string="Ref. Llenado", comodel_name="product.product")
    llenado_fecha = fields.Datetime(string="Fecha Llenado")
    celda_num = fields.Float(string="Num. Celda", index=True, digits=(15, 0))
    product_id = fields.Many2one(string="Ref. Celda", comodel_name="product.product")
    celda_fecha = fields.Datetime(string="Fecha Celda")
    num_secciona = fields.Integer(string="Numero de Seccionadores")
    enclavamientos = fields.Boolean(default=False)
    inspec_visual = fields.Boolean(string="Inspeccion Visual", default=False)
    niv_fuga_max = fields.Float(string="Nivel de fuga maximo", digits=(9, 10))
    niv_llen_min = fields.Float(string="Nivel llenado final minimo", digits=(9, 2))
    niv_fuga_med = fields.Float(string="Nivel de fuga medido", digits=(9, 10))
    niv_llen_med = fields.Float(string="Nivel llenado final medido", digits=(9, 2))
    peso_sf6 = fields.Integer(string="Peso SF6")
    ensayo_llenado = fields.Boolean(string="Ensayado Llenado", default=False)
    v_ens_tierra = fields.Integer(string="V ensayo a tierra")
    v_ens_bobina = fields.Integer(string="V ensayo bobina")
    v_ens_circu = fields.Integer(string="V ensayo circuitos auxiliares")
    v_supe_disparo1 = fields.Float(string="V superior disparo 1", digits=(9, 2))
    v_infe_disparo1 = fields.Float(string="V inferior disparo 1", digits=(9, 2))
    v_supe_disparo2 = fields.Float(string="V superior disparo 2", digits=(9, 2))
    v_infe_disparo2 = fields.Float(string="V inferior disparo 2", digits=(9, 2))
    tiempo_dis_max = fields.Integer(string="Tiempo disparo maximo")
    ens_tierra = fields.Boolean(string="Ensayo a tierra", default=False)
    ens_bobina = fields.Boolean(string="Ensayo bobina", default=False)
    ens_circu = fields.Boolean(string="Ensayo circuitos auxiliares", default=False)
    ens_disparo1 = fields.Boolean(string="Ensayo disparo 1", default=False)
    ens_disparo2 = fields.Boolean(string="Ensayo disparo 2", default=False)
    tiempo_dis_medido = fields.Float(string="Tiempo disparo medido", digits=(6, 2))
    i2t_disparo = fields.Float(string="i2t disparo", digit=(8, 2))
    fecha_dielectrico = fields.Datetime(string="Fecha ensayo dielectrico")
    ens_dielectrico = fields.Boolean(string="Ensayado dielectrico", default=False)
    conce_max = fields.Float(string="Concentracion maxima", digits=(8, 2))
    conce_medida = fields.Float(string="Concentracion medida", digits=(8, 3))
    fecha_embolsa = fields.Datetime(string="Fecha embolsamiento")
    ens_embolsa = fields.Boolean(string="Ensayado embolsamiento", default=False)
    lineas_ids = fields.One2many(
        string="Lineas de Seccionadores",
        comodel_name="res.celdas.seccionadores",
        inverse_name="celda_id",
    )
    c_orden = fields.Integer(string="Orden Celda")
    nota = fields.Char()
    production_id = fields.Many2one(
        string="O.F. Celda",
        comodel_name="mrp.production",
    )
    llenado_fecha_ens = fields.Datetime(string="Fecha Ensayo Llenado")
    production_premo_id = fields.Many2one(
        string="O.F. Premo", comodel_name="mrp.production"
    )
    production_llena_id = fields.Many2one(
        string="O.F. Llenado",
        comodel_name="mrp.production",
    )
    production_monta_id = fields.Many2one(
        string="O.F. Montaje", comodel_name="mrp.production"
    )
    lineas_conex_ids = fields.One2many(
        string="Lineas de Conexiones",
        comodel_name="res.celdas.conexiones",
        inverse_name="celda_id",
    )
    lineas_equip_ids = fields.One2many(
        string="Lineas de Equipos",
        comodel_name="res.celdas.equipos",
        inverse_name="celda_id",
    )
