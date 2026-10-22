# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

from odoo.addons.ina_mp_lat_res_ensayos.lat_lot_migration import (
    clear_converted,
    keep_serial_in_name,
    rename_in_filters,
    serial_to_lot,
    set_tracking,
)

SERIALS = {
    "res_aisladores": "num_serie",
    "res_basescutout": "num_serie",
    "res_celdas": "celda_num",
    "res_enlaces": "name",
    "res_fusibles": "num_serie",
    "res_pararrayos": "num_serie",
    "res_seccionadores": "num_serie",
    "res_seccionalizadores": "num_serie",
    "res_trafos": "num_serie",
}
COMPONENTS = ("res_celdas_equipos", "res_celdas_conexiones")


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("base.group_user")._apply_group(env.ref("stock.group_production_lot"))
    product_ids = set()
    for table, column in SERIALS.items():
        product_ids |= serial_to_lot(cr, table, column)
        if column != "name":
            keep_serial_in_name(cr, table, column)
            rename_in_filters(cr, table.replace("_", "."), column, "lot_id")
    set_tracking(env, product_ids)
    product_ids = set()
    for table in COMPONENTS:
        product_ids |= serial_to_lot(cr, table, "num_serie")
        clear_converted(cr, table, "num_serie")
        rename_in_filters(cr, table.replace("_", "."), "num_serie", "lot_id")
    set_tracking(env, product_ids, "lot")
