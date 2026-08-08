# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_ver_stock(self):
        return True
        # return self.mapped("product_id").action_open_quants()
