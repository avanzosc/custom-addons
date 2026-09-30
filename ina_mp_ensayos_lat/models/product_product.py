# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_ver_ensayos(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "ina_mp_ensayos_lat.action_ina_mrp_ensayos_prod"
        )
        action["context"] = {"default_product_id": self.id}
        action["domain"] = [("product_id", "=", self.id)]
        return action
