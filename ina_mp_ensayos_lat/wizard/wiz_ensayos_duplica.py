# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WizEnsayosDuplica(models.TransientModel):
    _name = "wiz.ensayos.duplica"

    product_id = fields.Many2one(
        string="Nuevo Producto",
        comodel_name="product.product",
        required=True,
        help="Crear todos los ensayos para este producto",
    )

    def wiz_duplica_ensayo(self):
        explo = self.env["mrp.ensayos.producto"]
        explo.duplica_ensayo(self.product_id)
