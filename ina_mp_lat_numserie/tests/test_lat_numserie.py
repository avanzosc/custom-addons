# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import Form, TransactionCase


class TestLatNumserie(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Pararrayos LAT", "is_storable": True}
        )
        cls.production = cls.env["mrp.production"].create(
            {"product_id": cls.product.id}
        )
        cls.lot = cls.env["stock.lot"].create(
            {"name": "261000001", "product_id": cls.product.id}
        )
        cls.env["res.pararrayos"].create(
            {
                "name": 261000001,
                "product_id": cls.product.id,
                "lot_id": cls.lot.id,
                "production_id": cls.production.id,
            }
        )
        partner = cls.env["res.partner"].create({"name": "Cliente LAT"})
        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [(0, 0, {"product_id": cls.product.id})],
            }
        )

    def _form(self):
        form = Form(self.env["lat.num"])
        form.ensayo = "pararrayos"
        form.venta_id = self.sale
        return form

    def test_lot_fills_test_data(self):
        form = self._form()
        with form.lineas_ids.new() as line:
            line.lot_id = self.lot
            self.assertEqual(line.product_id, self.product)
            self.assertEqual(line.production_id, self.production)
            self.assertEqual(line.linea_venta_id, self.sale.order_line)
        num = form.save()
        self.assertEqual(self.lot.lat_numserie_ids, num.lineas_ids)

    def test_lot_without_test(self):
        lot = self.env["stock.lot"].create(
            {"name": "261000002", "product_id": self.product.id}
        )
        form = self._form()
        with form.lineas_ids.new() as line:
            line.lot_id = lot
            self.assertFalse(line.lot_id)
            self.assertFalse(line.product_id)
