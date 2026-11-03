# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

RESINA_GROUPS = (
    "ina_mc_permisos.group_inael_lat_user,ina_mc_permisos.group_inael_fabrica_user"
)


class StockLot(models.Model):
    _inherit = "stock.lot"

    lat_inyeccion_ids = fields.One2many(
        string="Inyecciones de Resina",
        comodel_name="res.inyeccion",
        inverse_name="lot_id",
        groups=RESINA_GROUPS,
    )
    lat_pts_ids = fields.One2many(
        string="Ensayos PTS",
        comodel_name="res.pts",
        inverse_name="lot_id",
        groups=RESINA_GROUPS,
    )
    lat_ppt_ids = fields.One2many(
        string="Ensayos PPT",
        comodel_name="res.ppt",
        inverse_name="lot_id",
        groups=RESINA_GROUPS,
    )
