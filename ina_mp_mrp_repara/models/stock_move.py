# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    coste = fields.Float(
        string="Precio Medio",
        related="product_id.standard_price",
        digits=(9, 2),
    )

    def _check_repair_product_fantasma(self):
        for move in self:
            if (
                move.repair_id
                and move.repair_line_type
                and move.product_id
                and move.product_id.fantasma
            ):
                raise UserError(_("Es un fantasma y no se permiten."))

    @api.constrains("repair_id", "repair_line_type", "product_id")
    def _check_repair_product_fantasma_constrains(self):
        self._check_repair_product_fantasma()

    @api.onchange("product_id", "repair_id", "repair_line_type")
    def _onchange_repair_product_fantasma(self):
        self._check_repair_product_fantasma()
        for move in self:
            if move.repair_id and move.repair_line_type and move.product_id:
                move.price_unit = move.product_id.standard_price

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                vals.get("repair_id")
                and vals.get("repair_line_type")
                and vals.get("product_id")
                and "price_unit" not in vals
            ):
                product = self.env["product.product"].browse(vals["product_id"])
                vals["price_unit"] = product.standard_price
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("product_id") and "price_unit" not in vals:
            repair_moves = self.filtered(lambda m: m.repair_id and m.repair_line_type)
            other_moves = self - repair_moves
            if not repair_moves:
                return super().write(vals)
            product = self.env["product.product"].browse(vals["product_id"])
            res = True
            if other_moves:
                res = super(StockMove, other_moves).write(vals)
            repair_vals = dict(vals, price_unit=product.standard_price)
            return super(StockMove, repair_moves).write(repair_vals) and res
        return super().write(vals)
