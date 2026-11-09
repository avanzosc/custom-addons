# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

from odoo.addons.ina_mp_lat_res_ensayos.lat_lot_migration import (
    clear_converted,
    rename_in_filters,
    serial_to_lot,
    set_tracking,
)

MODULE = "ina_mp_lat_resina"
MODELS = ["res.inyeccion", "res.mezcla", "res.ppt", "res.pts"]
SERIALS = {
    "res_inyeccion": ("num_serie", "product_id"),
    "res_pts": ("num_serie2", "product_id2"),
    "res_ppt": ("num_serie3", "product_id3"),
}


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    views = (
        env["ir.ui.view"]
        .with_context(active_test=False)
        .search([("model", "in", MODELS), ("active", "=", False)])
    )
    view_xmlids = views._get_external_ids()
    views.filtered(
        lambda view: any(
            xmlid.startswith(f"{MODULE}.") for xmlid in view_xmlids[view.id]
        )
    ).write({"active": True})
    rules = env["ir.model.access"].search([("model_id.model", "in", MODELS)])
    xmlids = rules.get_external_id()
    rules.filtered(lambda rule: not xmlids[rule.id]).unlink()
    product_ids = set()
    for table, (column, product_column) in SERIALS.items():
        product_ids |= serial_to_lot(cr, table, column, product_column)
        clear_converted(cr, table, column)
        rename_in_filters(cr, table.replace("_", "."), column, "lot_id")
    set_tracking(env, product_ids, "lot")
