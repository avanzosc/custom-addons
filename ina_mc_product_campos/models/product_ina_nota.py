# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductInaNota(models.Model):
    _name = "product.ina.nota"
    _description = "Nota del producto para Factura"
    _order = "secuencia"

    secuencia = fields.Integer(
        default=99, help="Secuencia para el orden de listado de la nota."
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Nota Factura",
        ondelete="cascade",
        index=True,
    )
    product_compon_id = fields.Many2one(
        comodel_name="product.product",
        string="Componente",
        help="Componente para incluir en la nota o vacio para descripcion" " adicional",
    )
    cantidad = fields.Float(digits="Product Unit of Measure")
    descripcion = fields.Char(
        help="Utilice este campo para añadir texto adicional", size=65
    )
    incluir_su_texto = fields.Boolean(
        string="Incluir su texto",
        default=False,
        help="Incluye la nota de factura de este producto si la tiene, "
        "(solo funcionara a 1 nivel)",
    )
