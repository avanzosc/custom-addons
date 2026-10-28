# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api

MODULE = "ina_md_ocr"
MODELS = ["inael.ocr", "inael.ocr.line", "ocr.docus"]


def migrate(cr, version):
    cr.execute("SELECT to_regclass('proyecto_order')")
    if cr.fetchone()[0]:
        cr.execute(
            """
            UPDATE inael_ocr o SET proyecto = p.name
            FROM proyecto_order p
            WHERE p.id = o.proyecto_legacy_id AND o.proyecto IS NULL
            """
        )
    env = api.Environment(cr, SUPERUSER_ID, {})
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
