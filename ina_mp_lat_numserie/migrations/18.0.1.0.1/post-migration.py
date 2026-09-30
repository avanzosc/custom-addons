# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

from odoo.addons.ina_mp_lat_res_ensayos.lat_lot_migration import (
    clear_converted,
    rename_in_filters,
    serial_to_lot,
    set_tracking,
)

TABLES = ("lat_numcentro", "lat_numcentro_lineas", "lat_numserie")


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    set_tracking(env, serial_to_lot(cr, "lat_numcentro", "numserie"))
    product_ids = serial_to_lot(cr, "lat_numcentro_lineas", "numserie")
    product_ids |= serial_to_lot(cr, "lat_numserie", "numserie")
    set_tracking(env, product_ids, "lot")
    for table in TABLES:
        clear_converted(cr, table, "numserie")
        rename_in_filters(cr, table.replace("_", "."), "numserie", "lot_id")
