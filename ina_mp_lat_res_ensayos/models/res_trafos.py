# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResTrafos(models.Model):
    _name = "res.trafos"
    _description = "LAT Resultados de ensayo de Trafos"

    name = fields.Float(string="Numero", digits=(15, 0))
    num_serie = fields.Char(string="Num. Serie")
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    normas = fields.Char()
    especi_tecnica = fields.Char(string="Especif. Tecnica")
    cliente = fields.Char()
    production_id = fields.Many2one(string="O.F.", comodel_name="mrp.production")
    potencia = fields.Integer()
    um = fields.Float(string="Um(kV) ", digits=(9, 1))
    frecuencia = fields.Integer()
    regula = fields.Char(string="Regulacion")
    simbo_acopla = fields.Char(string="Simbolo Acoplamiento")
    pot_acus_max = fields.Integer(string="Potencia acustica maxima [dB(A)]")
    tension_asi_at1 = fields.Integer(string="Tension AT1(V)")
    tension_asi_at2 = fields.Integer(string="Tension AT2(V)")
    tension_asi_bt2 = fields.Integer(string="Tension BT2(V)")
    tension_asi_bt3 = fields.Integer(string="Tension BT3(V)")
    corrien_asi_at1 = fields.Float(string="Corriente AT1(A)", digits=(9, 2))
    corrien_asi_at2 = fields.Float(string="Corriente AT2(A)", digits=(9, 2))
    corrien_asi_bt2 = fields.Float(string="Corriente BT2(A)", digits=(9, 2))
    corrien_asi_bt3 = fields.Float(string="Corriente BT3(A)", digits=(9, 2))
    factor_reduc = fields.Integer(string="Factor de Reduccion")
    vol_liq_ais = fields.Integer(string="Volumen Liquido Aislante(I)")
    masa_desencu = fields.Integer(string="Masa a desencubar(Kg)")
    masa_total = fields.Integer(string="Masa (Kg)")
    masa_bobin = fields.Integer(string="Masa Bobinados(Kg)")
    masa_nucleo = fields.Integer(string="Masa Nucleo(Kg)")
    liquido_ais = fields.Char(string="Liquido Aislante")
    densidad_ace = fields.Float(string="Densidad Aceite")
    fecha = fields.Datetime()
    temper = fields.Float(string="Temperatura(ºC)", digits=(9, 2))
    fecha_resis = fields.Datetime(string="Fecha Ensayo Resist.")
    pos_at1 = fields.Integer(string="Posicion AT1")
    pos_at2 = fields.Integer(string="Posicion AT2")
    pos_bt2 = fields.Integer(string="Posicion BT2")
    pos_bt3 = fields.Integer(string="Posicion BT3")
    res_at1_1uv = fields.Float(string="Rest. AT1 1U-1V", digits=(9, 4))
    res_at2_1uv = fields.Float(string="Rest. AT2 1U-1V", digits=(9, 4))
    res_bt2_2uv = fields.Float(string="Rest. BT2 2U-2V", digits=(9, 4))
    res_bt3_2uv = fields.Float(string="Rest. BT3 3U-3V", digits=(9, 4))
    res_at1_1vw = fields.Float(string="Rest. AT1 1V-1W", digits=(9, 4))
    res_at2_1vw = fields.Float(string="Rest. AT2 1V-1W", digits=(9, 4))
    res_bt2_2vw = fields.Float(string="Rest. BT2 2V-2W", digits=(9, 4))
    res_bt3_2vw = fields.Float(string="Rest. BT3 3V-3W", digits=(9, 4))
    res_at1_1wu = fields.Float(string="Rest. AT1 1W-1U", digits=(9, 4))
    res_at2_1wu = fields.Float(string="Rest. AT2 1W-1U", digits=(9, 4))
    res_bt2_2wu = fields.Float(string="Rest. BT2 2W-2U", digits=(9, 4))
    res_bt3_2wu = fields.Float(string="Rest. BT3 3W-3U", digits=(9, 4))
    lineas_rela_ids = fields.One2many(
        string="Lineas de Relacion",
        comodel_name="res.trafos.relacion",
        inverse_name="trafo_id",
    )
    lineas_vacio_ids = fields.One2many(
        string="Lineas de Vacio",
        comodel_name="res.trafos.vacio",
        inverse_name="trafo_id",
    )
    lineas_corto_ids = fields.One2many(
        string="Lineas de Corto",
        comodel_name="res.trafos.corto",
        inverse_name="trafo_id",
    )
    lineas_dielectrico_ids = fields.One2many(
        string="Lineas de Dielectrico",
        comodel_name="res.trafos.dielectrico",
        inverse_name="trafo_id",
    )
    lineas_resultados_ids = fields.One2many(
        string="Lineas de Resultados",
        comodel_name="res.trafos.resultados",
        inverse_name="trafo_id",
    )
    lineas_equipos_ids = fields.One2many(
        string="Lineas de Equipos",
        comodel_name="res.trafos.equipos",
        inverse_name="trafo_id",
    )
    tipo = fields.Char()
    nota = fields.Text(string="Notas")
    mat_at_bt = fields.Char(string="Material conductor AT/BT")
    mat_cir_mag = fields.Char(string="Material Circuito Magnetico")
    inspec_tapas = fields.Boolean(string="Inspecion de tapas", default=False)
    num_nucleo = fields.Char(string="Num. Nucleo")
    num_bob1 = fields.Char(string="Num. Bobina 1")
    num_bob2 = fields.Char(string="Num. Bobina 2")
    num_bob3 = fields.Char(string="Num. Bobina 3")
    esp_bobin = fields.Boolean(string="Espesor Bobinado BT", default=False)
    fecha_espesor = fields.Datetime()
    fecha_entbob_horno = fields.Datetime(string="Entrada en Horno")
    fecha_salbob_horno = fields.Datetime(string="Salida de Horno")
    mega_nuc = fields.Integer(string="Megado Nucleo")
    fecha_meg_nuc = fields.Datetime(string="Fecha Megado Nucleo")
    mega_bob1 = fields.Integer(string="Megado Bobina 1")
    mega_bob2 = fields.Integer(string="Megado Bobina 2")
    mega_bob3 = fields.Integer(string="Megado Bobina 3")
    fecha_meg_bob = fields.Datetime(string="Fecha Megado Bobinas")
    mega_cul = fields.Boolean(string="Montaje Culata", default=False)
    fecha_meg_cul = fields.Datetime(string="Fecha Montaje Culata")
    mega_mon_bobcul = fields.Integer(string="Megado Mont. Bob+culata")
    fecha_meg_mon_bobcul = fields.Datetime(string="Fecha Megado Bob+culata")
    conex_abt = fields.Boolean(string="Conexionado Parte Activa", default=False)
    fecha_conex_abt = fields.Datetime(string="Fecha Conexiones")
    rela_transf = fields.Boolean(string="Relacion Transformacion OK")
    resis_un = fields.Float(string="Resist. U-N")
    resis_vn = fields.Float(string="Resist. V-N")
    resis_wn = fields.Float(string="Resist. W-N")
    resis_uv = fields.Float(string="Resist. U-V")
    resis_uw = fields.Float(string="Resist. U-W")
    resis_vw = fields.Float(string="Resist. V-W")
    num_tapa = fields.Char(string="Num. Tapa")
    fecha_entcur_horno = fields.Datetime(string="Entrada en Horno")
    fecha_salcur_horno = fields.Datetime(string="Salida de Horno")
    ensay_aisla = fields.Char(string="Nivel Aislamiento")
    tipo_ace = fields.Char(string="Tipo Aceite")
    num_cuba = fields.Char(string="Num. Cuba")
    fecha_encubado = fields.Datetime()
    fecha_pares = fields.Datetime(string="Fecha Pares Apriete")
    peso_activa = fields.Float(string="Peso Parte Activa")
    fecha_ini_llenado = fields.Datetime(string="Inicio Llenado Aceite")
    fecha_fin_llenado = fields.Datetime(string="Final Llenado Aceite")
    fecha_ini_vacio = fields.Datetime(string="Inicio Vacio")
    fecha_fin_vacio = fields.Datetime(string="Final Vacio ")
    fecha_ini_reposo = fields.Datetime(string="Inicio Reposo")
    fecha_fin_reposo = fields.Datetime(string="Final Reposo")
    temp_aceite = fields.Float(string="Temp. Aceite")
    lit_aceite = fields.Float(string="Litros Aceite")
    peso_total = fields.Float()
    line_documen_ids = fields.One2many(
        string="Documen. Trafos",
        comodel_name="trafos.inspec.docus",
        inverse_name="trafo_id",
    )
