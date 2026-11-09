# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

from odoo.addons.ina_mp_lat_res_ensayos.models.stock_lot import LAT_GROUPS


class StockLot(models.Model):
    _inherit = "stock.lot"

    lat_numcentro_ids = fields.One2many(
        string="Centro",
        comodel_name="lat.numcentro",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_numcentro_linea_ids = fields.One2many(
        string="Montado en Centros",
        comodel_name="lat.numcentro.lineas",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
    lat_numserie_ids = fields.One2many(
        string="Numeros de Serie en Ordenes de Venta",
        comodel_name="lat.numserie",
        inverse_name="lot_id",
        groups=LAT_GROUPS,
    )
