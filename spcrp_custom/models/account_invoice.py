# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_logo_to_print(self):
        make_obj = self.env["product.make"]
        for invoice in self:
            makes = invoice.invoice_line_ids.filtered("make_id").mapped("make_id")
            if len(makes) == 1:
                make = makes[0]
                if make.logo:
                    invoice.logo_to_print = make.logo
                    invoice.three_address_in_invoice_report = (
                        make.three_address_in_invoice_report
                    )
                else:
                    search_default_logo = True
            else:
                search_default_logo = False
            if len(makes) == 2:
                makes2 = invoice.invoice_line_ids.filtered(
                    lambda z: z.make_id.common_logo
                ).mapped("make_id")
                if len(makes2) == 2:
                    invoice.logo_to_print = makes2[0].common_logo
                    invoice.three_address_in_invoice_report = True
                else:
                    search_default_logo = True
            if not makes or len(makes) > 3 or search_default_logo:
                make = make_obj.search([("use_logo", "=", True)], limit=1)
                company = self.env.user.company_id
                invoice.logo_to_print = make.logo if make else company.logo
                invoice.three_address_in_invoice_report = (
                    make.three_address_in_invoice_report if make else True
                )


    logo_to_print = fields.Binary("Image", compute="_compute_logo_to_print")
    three_address_in_sale_report = fields.Boolean(
        string="Show all three addresses in sales reports ",
        compute="_compute_logo_to_print",
    )
    city = fields.Char(string="City", related="partner_id.city", store=True)
    state_id = fields.Many2one(
        string="Province",
        comodel_name="res.country.state",
        related="partner_id.state_id",
        store=True,
    )
    shipping_city = fields.Char(
        string="Shipping city", related="partner_shipping_id.city", store=True
    )
    shipping_state_id = fields.Many2one(
        string="Shipping province",
        comodel_name="res.country.state",
        related="partner_shipping_id.state_id",
        store=True,
    )

    def action_makes_in_lines(self):
        result = super().action_makes_in_lines()
        self.update_division_in_invoices()
        return result
