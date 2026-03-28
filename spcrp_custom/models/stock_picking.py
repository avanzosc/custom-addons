# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_text_delivery_vouchers(self):
        values = self.env["res.config.settings"].sudo().get_values()
        for picking in self:
            picking.text_delivery_vouchers = values.get("text_delivery_vouchers", " ")

    def _compute_print_make_sector(self):
        cond = [("print_make_on_out_picking", "=", True)]
        makes = self.env["product.make"].search(cond)
        for picking in self.filtered(lambda x: x.picking_type_id.code == "outgoing"):
            make_to_print = ""
            sector_to_print = ""
            for make in makes:
                if make.name in picking.makes_in_lines:
                    make_to_print = make.name
                    if (
                        make.market_to_print_ids
                        and picking.market_id in make.market_to_print_ids
                    ):
                        sector_to_print = picking.market_id.name
            if make_to_print:
                picking.make_to_print = make_to_print
            if sector_to_print:
                picking.sector_to_print = sector_to_print

    @api.depends(
        "move_line_ids_without_package",
        "move_line_ids_without_package.product_shipping_length",
    )
    def _compute_shipping_length(self):
        for picking in self:
            volume = 0.0
            for line in picking.move_line_ids_without_package:
                if line.product_shipping_length > volume:
                    volume = line.product_shipping_length
            picking.shipping_length = volume



    text_delivery_vouchers = fields.Text(
        string="Text for delivery vouchers", compute="_compute_text_delivery_vouchers"
    )
    make_to_print = fields.Char(
        string="Make to print", compute="_compute_print_make_sector"
    )
    sector_to_print = fields.Char(
        string="Sector to print", compute="_compute_print_make_sector"
    )
    shipping_type_id = fields.Many2one(
        string="Shipping type", comodel_name="stock.picking.shipping.type"
    )
    shipping_length = fields.Float(
        string="Length", compute="_compute_shipping_length", store=True
    )
    contact_email_person_id = fields.Many2one(
        string="Contact email person", comodel_name="res.partner"
    )
    picking_type_code = fields.Selection(
        string="Type of Operation",
        related="picking_type_id.code",
        store=True,
        copy=False,
    )
    confirmation_email_sent = fields.Boolean(
        string="Confirmation email sent", default=False, copy=False
    )
    cost_of_transportation = fields.Monetary(
        string="Cost of transportation", copy=False, default=0.0, digits="Product Price"
    )
    weight = fields.Float(string="Net weight")
    gross_weight = fields.Float(string="Gross weight", default=0, copy=False)

    def action_makes_in_lines(self):
        result = super().action_makes_in_lines()
        self.update_division_in_pickings()
        return result
