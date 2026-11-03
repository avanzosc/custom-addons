# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_ver_stock(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.location_open_quants"
        )
        action["domain"] = [("product_id", "in", self.ids)]
        action["context"] = {
            "search_default_locationgroup": 1,
            "search_default_internal_loc": 1,
        }
        return action
