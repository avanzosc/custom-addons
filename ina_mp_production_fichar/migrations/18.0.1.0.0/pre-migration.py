# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.ina_mp_production_fichar.hooks import keep_legacy_laser_ids


def migrate(cr, version):
    keep_legacy_laser_ids(cr)
