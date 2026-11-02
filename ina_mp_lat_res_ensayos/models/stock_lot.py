# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

LAT_GROUPS = (
    "ina_mc_permisos.group_inael_lat_user,"
    "ina_mc_permisos.group_inael_calidad_respon,"
    "ina_mc_permisos.group_inael_fabrica_respon"
)


class StockLot(models.Model):
    _inherit = "stock.lot"

    lat_aisladores_ids = fields.One2many(
        string="Ensayos de Aisladores",
        comodel_name="res.aisladores",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_basescutout_ids = fields.One2many(
        string="Ensayos de Bases y Cutout",
        comodel_name="res.basescutout",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_celdas_ids = fields.One2many(
        string="Ensayos de Celdas",
        comodel_name="res.celdas",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_celdas_conexion_ids = fields.One2many(
        string="Conexiones en Celdas",
        comodel_name="res.celdas.conexiones",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_celdas_equipo_ids = fields.One2many(
        string="Montado en Celdas",
        comodel_name="res.celdas.equipos",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_enlaces_ids = fields.One2many(
        string="Ensayos de Enlaces",
        comodel_name="res.enlaces",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_fusibles_ids = fields.One2many(
        string="Ensayos de Fusibles",
        comodel_name="res.fusibles",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_pararrayos_ids = fields.One2many(
        string="Ensayos de Pararrayos",
        comodel_name="res.pararrayos",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_seccionadores_ids = fields.One2many(
        string="Ensayos de Seccionadores",
        comodel_name="res.seccionadores",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_seccionalizadores_ids = fields.One2many(
        string="Ensayos de Seccionalizadores",
        comodel_name="res.seccionalizadores",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_trafos_ids = fields.One2many(
        string="Ensayos de Trafos",
        comodel_name="res.trafos",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
