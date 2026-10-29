# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    automatic_barcode = fields.Boolean(
        default=False,
        help="Automatic barcode only",
    )

    def write(self, vals):
        res = super().write(vals)
        if vals.get("automatic_barcode") is True:
            get_param = self.env["ir.config_parameter"].sudo().get_param
            if self.product_variant_count > 0:
                for variant in self.product_variant_ids:
                    if variant.barcode:
                        continue
                    num, sequence = variant.generate_12_numbers_ean(get_param)
                    digit = variant.calculate_checksum(num)
                    num.append(digit)
                    barcode = "".join(map(str, num))
                    final_number_sequence = int(
                        get_param("product.default_final_number_sequence")
                    )
                    variant.write(
                        {
                            "barcode": barcode,
                            "difference_code_ean": (
                                final_number_sequence - int(sequence)
                            ),
                        }
                    )
                    difference_number = int(
                        get_param("product.default_difference_number")
                    )
                    if variant.difference_code_ean < difference_number:
                        email_next_visit = self.env.ref(
                            "mot_product_ean_automatic.email_ean_code"
                        )
                        email_next_visit.send_mail(variant.id)
        return res
