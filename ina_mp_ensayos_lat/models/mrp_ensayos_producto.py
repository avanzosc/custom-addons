# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, exceptions, fields, models

import odoo.addons.decimal_precision as dp


class MrpEnsayosProducto(models.Model):
    _name = "mrp.ensayos.producto"
    _description = "Ensayos LAT por producto"

    #   name  = fields.Char("Nombre")
    product_id = fields.Many2one(
        string="Producto", comodel_name="product.product", required=True, store=True
    )
    ensayo_id = fields.Many2one(
        string="Ensayo", comodel_name="mrp.ensayos", required=True, store=True
    )
    nominal = fields.Float(
        string="Valor Nominal",
        digits=dp.get_precision("Product Unit of Measure"),
        default=1,
        required=True,
    )
    minimo = fields.Float(
        string="Valor Minimo",
        digits=dp.get_precision("Product Unit of Measure"),
        default=1,
        required=True,
    )
    maximo = fields.Float(
        string="Valor Maximo",
        digits=dp.get_precision("Product Unit of Measure"),
        default=1,
        required=True,
    )
    etiqueta = fields.Char()
    nota = fields.Text()

    def duplica_ensayo(self, nuevo_producto):
        active_ids = self.env.context.get("active_ids", [])
        if len(active_ids) > 1:
            raise exceptions.ValidationError(
                _("Debes marcar solamente 1 producto/ensayo")
            )
        dup_obj = self.env["mrp.ensayos.producto"]
        cond = [("product_id", "=", nuevo_producto.id)]
        d_ids = dup_obj.search(cond)
        if d_ids:
            raise exceptions.ValidationError(_("Este nuevo producto ya tiene ensayos"))
        for e in dup_obj.browse(self.env.context.get("active_ids")):
            cond = [("product_id", "=", e.product_id.id)]
            d_ids = dup_obj.search(cond)
            for r in d_ids:
                val = {
                    "product_id": nuevo_producto.id,
                    "ensayo_id": r.ensayo_id.id,
                    "nominal": r.nominal,
                    "minimo": r.minimo,
                    "maximo": r.maximo,
                    "etiqueta": r.etiqueta,
                    "nota": r.nota,
                }
                dup_obj.create(val)
        return True
