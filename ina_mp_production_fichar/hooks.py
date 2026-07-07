# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo.tools.sql import column_exists, table_exists

_logger = logging.getLogger(__name__)

MODULE = "ina_mp_production_fichar"
MODELS = ["hr.employee.fichar", "hr.fichar.historico", "hr.puesto.fichar"]


def pre_init_hook(env):
    if table_exists(env.cr, "hr_employee_fichar"):
        keep_legacy_laser_ids(env.cr)


def post_init_hook(env):
    activate_legacy_records(env)


def keep_legacy_laser_ids(cr):
    if column_exists(cr, "hr_employee_fichar", "laser_legacy_id"):
        return
    cr.execute(
        "ALTER TABLE hr_employee_fichar "
        "DROP CONSTRAINT IF EXISTS hr_employee_fichar_laser_id_fkey"
    )
    cr.execute("ALTER TABLE hr_employee_fichar ADD COLUMN laser_legacy_id integer")
    cr.execute(
        """
        UPDATE hr_employee_fichar
           SET laser_legacy_id = laser_id,
               laser_id = NULL
         WHERE laser_id IS NOT NULL
        """
    )
    _logger.info("order.olaser ids kept in laser_legacy_id on %s rows", cr.rowcount)


def activate_legacy_records(env):
    cr = env.cr
    prefix = f"{MODULE}."
    names = [
        xmlid[len(prefix) :]
        for xmlid in env.registry.loaded_xmlids
        if xmlid.startswith(prefix)
    ]
    view_data = env["ir.model.data"].search(
        [
            ("module", "=", MODULE),
            ("model", "=", "ir.ui.view"),
            ("name", "in", names),
        ]
    )
    views = (
        env["ir.ui.view"]
        .with_context(active_test=False)
        .browse(view_data.mapped("res_id"))
    )
    views.filtered(lambda view: not view.active).write({"active": True})
    rules = env["ir.model.access"].search([("model_id.model", "in", MODELS)])
    xmlids = rules.get_external_id()
    rules.filtered(lambda rule: not xmlids[rule.id]).unlink()
    if column_exists(cr, "hr_employee_fichar", "improductivo_moved0"):
        cr.execute("SELECT count(improductivo_moved0) FROM hr_employee_fichar")
        if not cr.fetchone()[0]:
            cr.execute("ALTER TABLE hr_employee_fichar DROP COLUMN improductivo_moved0")
