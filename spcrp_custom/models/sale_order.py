# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_logo_to_print(self):
        make_obj = self.env["product.make"]
        for sale in self:
            makes = sale.order_line.filtered("make_id").mapped("make_id")
            if len(makes) == 1:
                make = makes[0]
                if make.logo:
                    sale.logo_to_print = make.logo
                    sale.three_address_in_sale_report = (
                        make.three_address_in_sale_report
                    )
                else:
                    search_default_logo = True
            else:
                search_default_logo = False
            if len(makes) == 2:
                makes2 = sale.order_line.filtered(
                    lambda x: x.make_id.common_logo
                ).mapped("make_id")
                if len(makes2) == 2:
                    sale.logo_to_print = makes2[0].common_logo
                    sale.three_address_in_sale_report = True
                else:
                    search_default_logo = True
            if not makes or len(makes) > 3 or search_default_logo:
                make = make_obj.search([("use_logo", "=", True)], limit=1)
                company = self.env.user.company_id
                sale.logo_to_print = make.logo if make else company.logo
                sale.three_address_in_sale_report = (
                    make.three_address_in_sale_report if make else True
                )



    logo_to_print = fields.Binary("Image", compute="_compute_logo_to_print")
    three_address_in_sale_report = fields.Boolean(
        string="Show all three addresses in sales reports ",
        compute="_compute_logo_to_print",
    )
    contact_email_person_id = fields.Many2one(
        string="Contact email person", comodel_name="res.partner"
    )

    @api.onchange("warehouse_id")
    def onchange_warehouse_id_spacorp_custom(self):
        if self.warehouse_id.sale_fiscal_position_id:
            self.fiscal_position_id = self.warehouse_id.sale_fiscal_position_id

    @api.onchange("type_id")
    def onchange_type_id(self):
        for order in self:
            if order.type_id and order.type_id.analytic_account_id:
                analytic_account = order.type_id.analytic_account_id
                order.analytic_account_id = analytic_account.id

    def action_confirm(self):
        for sale in self:
            error = ""
            if (
                sale.partner_id.is_company
                and sale.partner_id.customer_rank
                and not sale.partner_id.contact_person
            ):
                error = _("You must indicate an 'Accounting contact' on the client.")
            if (
                sale.partner_id.customer_rank
                and not sale.partner_id.email
                and sale.partner_id.show_children_email
            ):
                lit = _("You must indicate an 'Accounting email' on the client.")
                error = lit if not error else "{}\n{}".format(error, lit)
            if (
                sale.partner_id.customer_rank
                and not sale.partner_id.email
                and not sale.partner_id.show_children_email
            ):
                lit = _("You must indicate an 'Email' on the client.")
                error = lit if not error else "{}\n{}".format(error, lit)
            if not sale.partner_id.vat:
                lit = _("The client does not have VAT.")
                error = lit if not error else "{}\n{}".format(error, lit)
            if error:
                raise exceptions.ValidationError(error)
        return super().action_confirm()

    def _create_delivery_line(self, carrier, price_unit):
        line = super()._create_delivery_line(carrier, price_unit)
        line.put_makes_in_line()
        return line

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        self.contact_email_person_id = self.partner_id
        return result

    def action_makes_in_lines(self):
        result = super().action_makes_in_lines()
        for sale in self:
            sale.update_division_in_sales()
        return result
