# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class InaLatLotBaseMixin(models.AbstractModel):
    _name = "ina.lat.lot.base.mixin"
    _description = "Numero de serie INAEL como lote de Odoo (base)"

    _lat_tracking = "serial"
    _lat_product_field = "product_id"

    lot_id = fields.Many2one(
        string="Numero de Serie",
        comodel_name="stock.lot",
        index="btree_not_null",
        ondelete="restrict",
        domain="[('product_id', '=?', product_id)]",
    )

    @api.constrains(lambda self: ("lot_id", self._lat_product_field))
    def _check_lot_id_product(self):
        for record in self.filtered("lot_id"):
            if record.lot_id.product_id != record[self._lat_product_field]:
                raise ValidationError(
                    _(
                        "El numero de serie %(lot)s es del producto %(product)s.",
                        lot=record.lot_id.name,
                        product=record.lot_id.product_id.display_name,
                    )
                )

    @api.onchange("lot_id")
    def _onchange_lot_id_product(self):
        if self.lot_id:
            self[self._lat_product_field] = self.lot_id.product_id

    def _clear_lot_of_other_product(self):
        if self.lot_id and self.lot_id.product_id != self[self._lat_product_field]:
            self.lot_id = False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._set_lat_product_tracking()
        return records

    def write(self, vals):
        result = super().write(vals)
        if vals.get("lot_id"):
            self._set_lat_product_tracking()
        return result

    def _set_lat_product_tracking(self):
        if not self._lat_tracking:
            return
        templates = self.lot_id.product_id.product_tmpl_id.filtered(
            lambda t: t.is_storable and t.tracking == "none"
        )
        if templates:
            templates.write({"tracking": self._lat_tracking})


class InaLatLotMixin(models.AbstractModel):
    _name = "ina.lat.lot.mixin"
    _inherit = ["ina.lat.lot.base.mixin"]
    _description = "Numero de serie INAEL como lote de Odoo"

    @api.onchange("product_id")
    def _onchange_product_id_lot(self):
        self._clear_lot_of_other_product()
