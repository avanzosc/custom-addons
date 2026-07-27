# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class OrderoLaserRechazo(models.Model):
    _name = "order.olaser.rechazo"
    _description = "Rechazos en olaser"

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
    cantidad = fields.Float(string="Cantidad rechazo", digits=(9, 2), required=True)
    procesado = fields.Boolean(default=False)

    @api.onchange("product_id")
    def onchange_product_id(self):
        existe = False if self.product_id else True
        for r in self.olaser_id.listas_ids:
            if r.product_id == self.product_id:
                existe = True
        if not existe:
            raise UserError(
                _("ATENCION!!! : Esta ref. %s no esta en la lista de esta orden.")
                % (self.product_id.default_code)
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get("product_id")
            olaser_id = vals.get("olaser_id")
            # si no hay producto no seguimos validando lista
            if not product_id or not olaser_id:
                continue
            olaser = self.env["order.olaser"].browse(olaser_id).exists()
            if not olaser:
                continue
            if olaser.state in ("done", "cancel"):
                raise UserError(
                    _("No se puede crear rechazos con estado Cancelado o Terminado")
                )
            existe = any(line.product_id.id == product_id for line in olaser.listas_ids)
            if not existe:
                raise UserError(
                    _("ATENCIÓN: la referencia no está en la lista de esta orden.")
                )
        return super().create(vals_list)

    def unlink(self):
        for rec in self:
            if rec.procesado:
                raise UserError(_("No puedes borrar un rechazo procesado."))
        return super().unlink()
