# Copyright 2019 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    logo_id = fields.Many2one(
        string="Logo",
        comodel_name="res.company.logo",
        default=lambda self: self.env["res.company.logo"].get_default_logo(),
    )


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        res = super()._get_new_picking_values()
        if self.sale_line_id:
            res["logo_id"] = self.sale_line_id.order_id.logo_id.id
        return res
