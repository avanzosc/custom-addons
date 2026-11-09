# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPts(models.Model):
    _name = "res.pts"
    _description = "Tabla de resina pts"
    _inherit = ["ina.lat.lot.base.mixin"]
    _lat_tracking = "lot"
    _lat_product_field = "product_id2"

    lot_id = fields.Many2one(domain="[('product_id', '=?', product_id2)]")

    num_serie2 = fields.Integer(
        string="Num. Serie Antiguo",
        readonly=True,
        help="Numero de las piezas PTS sin producto, que no tienen lote.",
    )
    production_id2 = fields.Many2one(string="O.F.", comodel_name="mrp.production")
    product_id2 = fields.Many2one(string="Producto", comodel_name="product.product")
    n_inyeccion = fields.Integer(string="Num. inyeccion")
    n_rosca = fields.Integer(string="Num. Rosca")
    rosca_pasa = fields.Boolean(string="Rosca pasa", default=False)
    rosca_nopasa = fields.Boolean(string="Rosca no pasa", default=False)
    continuidad = fields.Boolean(string="Continuidad OK", default=False)
    baja10pc = fields.Integer(string="Bajada 10 pC (kV)")
    baja21kv = fields.Boolean(string="Bajada 21.8 kV <5pC", default=False)
    baja31 = fields.Boolean(string="Bajada 31.2 kV <10pC", default=False)
    tension = fields.Integer(string="Frecuencia Industrial (kV)")
    rechazo = fields.Char()
    valido = fields.Boolean(default=False)
    fecha_ensayo = fields.Datetime()
    nota2 = fields.Char(string="Notas")

    @api.onchange("product_id2")
    def _onchange_product_id2_lot(self):
        self._clear_lot_of_other_product()
