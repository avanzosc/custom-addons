# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from odoo.addons.ina_mp_lat_res_ensayos.models.stock_lot import LAT_GROUPS


class StockLot(models.Model):
    _inherit = "stock.lot"

    lat_especificacion_count = fields.Integer(
        string="Especificaciones de Ensayo",
        compute="_compute_lat_especificacion_count",
        groups=LAT_GROUPS,
    )

    @api.depends("product_id")
    def _compute_lat_especificacion_count(self):
        groups = self.env["mrp.ensayos.producto"]._read_group(
            [("product_id", "in", self.product_id.ids)], ["product_id"], ["__count"]
        )
        counts = {product.id: count for product, count in groups}
        for lot in self:
            lot.lat_especificacion_count = counts.get(lot.product_id.id, 0)

    def action_lat_ver_especificaciones(self):
        self.ensure_one()
        return self.product_id.action_ver_ensayos()
