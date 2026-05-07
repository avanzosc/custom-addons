# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_logo_to_print(self):
        make_obj = self.env["product.make"]
        for sale in self:
            makes = make_obj
            search_default_logo = False
            for line in sale.order_line.filtered(lambda x: x.make_id):
                if line.make_id not in makes:
                    makes += line.make_id
            if len(makes) == 1:
                if makes.logo:
                    sale.logo_to_print = makes.logo
                    sale.three_address_in_sale_report = (
                        makes.three_address_in_sale_report
                    )
                if not makes.logo:
                    search_default_logo = True
            if len(makes) == 2:
                makes2 = make_obj
                lines = sale.order_line.filtered(
                    lambda x: x.make_id and x.make_id.common_logo
                )
                for line in lines:
                    if line.make_id not in makes2:
                        makes2 += line.make_id
                if len(makes2) == 2:
                    sale.logo_to_print = makes2[0].common_logo
                    sale.three_address_in_sale_report = True
                else:
                    search_default_logo = True
            if len(makes) == 0 or len(makes) > 3 or search_default_logo:
                cond = [("use_logo", "=", True)]
                make = make_obj.search(cond, limit=1)
                if make:
                    sale.logo_to_print = make.logo
                    sale.three_address_in_sale_report = (
                        make.three_address_in_sale_report
                    )
                else:
                    sale.logo_to_print = self.env.user.company_id.logo
                    sale.three_address_in_sale_report = True

    logo_to_print = fields.Binary(string="Image", compute="_compute_logo_to_print")
    three_address_in_sale_report = fields.Boolean(
        string="Show all three addresses in sales reports",
        compute="_compute_logo_to_print",
    )
