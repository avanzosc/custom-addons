# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = "Product Product Inherit"

    difference_code_ean = fields.Float(string="Difference code EAN")

    @api.model_create_multi
    def create(self, vals_list):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        products = super().create(vals_list)
        for product in products:
            product_template = self.env["product.template"].search(
                [("product_variant_ids", "=", product.id)]
            )
            if (
                not product.barcode
                and product_template
                and product_template.automatic_barcode
            ):
                num, sequence = self.generate_12_numbers_ean(get_param)
                digit = self.calculate_checksum(num)
                num.append(digit)
                barcode = "".join(map(str, num))

                final_number_sequence = int(
                    get_param("product.default_final_number_sequence")
                )

                product.write(
                    {
                        "barcode": barcode,
                        "difference_code_ean": (final_number_sequence - int(sequence)),
                    }
                )
                difference_number = int(get_param("product.default_difference_number"))
                if product.difference_code_ean < difference_number:
                    email_next_visit = self.env.ref(
                        "mot_product_ean_automatic.email_ean_code"
                    )
                    email_next_visit.send_mail(product.id)
        return products

    def generate_12_numbers_ean(self, get_param):
        country_number_code = self.env.company.country_company_code
        company_number_code = self.env.company.company_code
        sequence_id = int(get_param("product.default_product_ean_sequence"))
        sequence = self.env["ir.sequence"].browse(sequence_id)._next()
        if not country_number_code or not company_number_code or not sequence:
            raise UserError(
                _(
                    "The country code, company code, or EAN generation "
                    "sequence is not configured. Please add them in "
                    "Settings / Companies."
                )
            )
        num = country_number_code + company_number_code + sequence
        num = [int(a) for a in num]
        if len(num) != 12:
            raise UserError(
                _(
                    "The generated EAN must contain exactly 12 digits "
                    "before calculating the check digit."
                )
            )
        return num, sequence

    def calculate_checksum(self, ean):
        assert len(ean) == 12, "EAN must contain 12 digits"
        evensum = sum(int(x) for x in ean[::2])
        oddsum = sum(int(x) for x in ean[1::2])
        return (10 - ((evensum + oddsum * 3) % 10)) % 10

    def get_code_ean_emails(self):
        user_group = self.env.ref("mot_product_ean_automatic.group_code_ean_product")
        email_list = [
            user.partner_id.email for user in user_group.users if user.partner_id.email
        ]
        return ",".join(email_list)
