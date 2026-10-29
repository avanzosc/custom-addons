# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _description = "Res Config Setting Inherit"

    country_number_code = fields.Char()
    company_number_code = fields.Char()
    sequence_ean_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Sequence EAN",
        config_parameter="product.default_product_ean_sequence",
    )
    final_number_sequence = fields.Char(
        config_parameter="product.default_final_number_sequence",
    )
    difference_number = fields.Char(
        string="Limit Difference Number",
        config_parameter="product.default_difference_number",
    )

    def set_values(self):
        company = self.env.company
        company.write(
            {
                "country_company_code": self.country_number_code,
                "company_code": self.company_number_code,
            }
        )
        return super().set_values()

    def get_values(self):
        company = self.env.company
        res = super().get_values()
        res.update(
            country_number_code=company.country_company_code,
            company_number_code=company.company_code,
        )
        return res
