# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

from odoo.addons.ina_mp_production_fichar.hooks import activate_legacy_records


def migrate(cr, version):
    activate_legacy_records(api.Environment(cr, SUPERUSER_ID, {}))
