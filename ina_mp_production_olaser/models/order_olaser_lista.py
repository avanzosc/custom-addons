# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class OrderoLaserLista(models.Model):
    _name = "order.olaser.lista"
    _description = "Referencias de olaser"

    olaser_id = fields.Many2one(
        comodel_name="order.olaser", string="olaser", ondelete="cascade"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        string="Producto",
        store=True,
        domain=[("tipo_comp_fab", "=", "corte")],
    )
    cantidad_chapa = fields.Float(string="Qty.Chapa", digits=(9, 2), required=True)
    cantidad_chapa_total = fields.Float(
        string="Qty.Chapa Total", digits=(9, 2), default=0, required=True
    )
    cantidad_consumo = fields.Float(
        string="Qty.Consumo Ud.", digits=(9, 2), required=True, help="segun LdM"
    )
    cantidad_consumo_total = fields.Float(
        string="Qty.Consumo Total", digits=(9, 2), required=True, help="segun LdM"
    )
    tiempo_ud = fields.Float(string="Tiempo Ud.", default=0, required=True)
    tiempo_total = fields.Float(default=0)
    cantidad_chapa_termi = fields.Float(
        string="Qty.Chapa Comunicada", digits=(9, 2), default=0
    )
    peso_gas = fields.Float(
        string="Peso Gas laser",
        digits="Product Unit of Measure",
        help="Peso del gas utilizado para cortar este producto. Se pondra "
        "solamente en el producto resultante que se introduce en la "
        "distribucion de corte.",
    )
    peso_gas_total = fields.Float(digits=(9, 2), default=0)
    plano = fields.Char(string="Nº Plano")

    @api.onchange("product_id")
    def onchange_product_id(self):
        self.cantidad_chapa = self.cantidad_chapa_total = 0
        self.tiempo_ud = 0
        self.peso_gas = self.product_id.peso_gas
        self.plano = self.product_id.plano
        cond = [("product_id", "=", self.product_id.id)]
        bom_ids = self.env["mrp.bom"].search(cond, limit=1)
        bom_id = bom_ids.id
        cond = [
            ("bom_id", "=", bom_id),
            ("product_id", "=", self.olaser_id.product_id.id),
        ]
        bom_line_ids = self.env["mrp.bom.line"].search(cond)
        if self.product_id and not bom_line_ids:
            # self.product_id=False
            raise UserError(
                _("ATENCION!!! : La MP %(mp)s no esta en la LdM de %(product)s")
                % {
                    "mp": self.product_id.default_code,
                    "product": self.olaser_id.product_id.default_code,
                }
            )
        self.cantidad_consumo = bom_line_ids.product_qty
        self.tiempo_ud = self.product_id.tiempo_chapa

    @api.onchange("cantidad_chapa", "cantidad_consumo")
    def onchange_cantidad_chapa(self):
        self.cantidad_chapa_total = self.olaser_id.cantidad * self.cantidad_chapa
        self.cantidad_consumo_total = self.cantidad_chapa * self.cantidad_consumo
        self.tiempo_total = self.cantidad_chapa_total * self.tiempo_ud
        self.peso_gas_total = self.peso_gas * self.cantidad_chapa_total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            wcom = vals.get("cantidad_consumo", 0)
            wchat = vals.get("cantidad_chapa_total", 0)
            wcomt = vals.get("cantidad_consumo_total", 0)
            if not wcom:
                raise UserError(_("La cantidad de consumo no puede ser cero."))
            if not wchat:
                raise UserError(_("La cantidad de chapa no puede ser cero."))
            if not wcomt:
                raise UserError(_("La cantidad de consumo total no puede ser cero."))
        return super().create(vals_list)
