# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    #   @api.onchange('default_code')
    #   def onchange_barcode(self):
    #       self.ensure_one()
    ##      res = super(ProductProduct, self).onchange_barcode()
    #       self.barcode=self.default_code

    # Estos campos son distintos, segun las variantes que tenga la template
    plano = fields.Char(size=15, copy=False)
    norma = fields.Char(size=30, copy=False)
    barcode = fields.Char(
        string="Barcode",
        oldname="ean13",
        related="default_code",
        readonly=True,
        store=True,
        copy=False,
    )
    nota_var = fields.Char(string="Nota Variante", copy=False)
