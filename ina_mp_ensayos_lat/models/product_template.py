# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_ver_ensayos(self):
        self.ensure_one()
        return self.product_variant_id.action_ver_ensayos()
