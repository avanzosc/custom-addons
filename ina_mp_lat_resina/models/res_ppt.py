# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPpt(models.Model):
    _name = "res.ppt"
    _description = "Tabla de resina ppt"
    _inherit = ["ina.lat.lot.base.mixin"]
    _lat_tracking = "lot"
    _lat_product_field = "product_id3"

    lot_id = fields.Many2one(domain="[('product_id', '=?', product_id3)]")

    num_serie3 = fields.Integer(
        string="Num. Serie Antiguo",
        readonly=True,
        help="Numero de las piezas PPT sin producto, que no tienen lote.",
    )
    production_id3 = fields.Many2one(string="O.F.", comodel_name="mrp.production")
    product_id3 = fields.Many2one(string="Producto", comodel_name="product.product")
    n_inyeccion2 = fields.Integer(string="Num. inyeccion")
    huella = fields.Integer()
    estanco = fields.Boolean(string="Estanqueidad (5 bar en agua)", default=False)
    inspeccion = fields.Char(string="Inspeccion Visual")
    valido2 = fields.Boolean(string="Valido", default=False)
    fecha_ensayo2 = fields.Datetime(string="Fecha Ensayo")
    nota3 = fields.Char(string="Notas")

    @api.onchange("product_id3")
    def _onchange_product_id3_lot(self):
        self._clear_lot_of_other_product()
