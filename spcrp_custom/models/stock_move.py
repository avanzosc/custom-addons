# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        result = super()._get_new_picking_values()
        if "origin" in result and result.get("origin", False):
            cond = [("name", "=", result.get("origin"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale and sale.contact_email_person_id:
                result["contact_email_person_id"] = sale.contact_email_person_id.id
        return result
