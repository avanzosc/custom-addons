# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_ver_ensayos(self):
        self.ensure_one()
        action = self.env.ref("ina_mp_ensayos_lat.action_ina_mrp_ensayos_prod")
        return {
            "name": action.name,
            "help": action.help,
            "type": action.type,
            "view_type": action.view_type,
            "view_mode": action.view_mode,
            "target": action.target,
            "res_model": action.res_model,
            "context": "{}",
            "domain": [("product_id", "=", self.product_variant_id.id)],
        }
