# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase

from odoo.addons.ina_mp_lat_res_ensayos.lat_lot_migration import serial_to_lot


class TestResinaLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pts = cls.env["product.product"].create(
            {"name": "Aislador PTS", "is_storable": True}
        )
        cls.ppt = cls.env["product.product"].create(
            {"name": "Aislador PPT", "is_storable": True}
        )

    def _lot(self, name, product):
        return self.env["stock.lot"].create({"name": name, "product_id": product.id})

    def test_pieza_and_inyeccion_lots(self):
        lot = self._lot("1102", self.pts)
        pieza = self.env["res.pts"].create(
            {"product_id2": self.pts.id, "lot_id": lot.id}
        )
        inyeccion = self.env["res.inyeccion"].create(
            {"product_id": self.pts.id, "lot_id": lot.id}
        )
        self.assertEqual(self.pts.tracking, "lot")
        self.assertEqual(lot.lat_pts_ids, pieza)
        self.assertEqual(lot.lat_inyeccion_ids, inyeccion)

    def test_lot_of_other_product(self):
        lot = self._lot("39804", self.ppt)
        with self.assertRaises(ValidationError):
            self.env["res.pts"].create({"product_id2": self.pts.id, "lot_id": lot.id})

    def test_onchanges_with_own_product_field(self):
        lot = self._lot("39804", self.ppt)
        form = Form(self.env["res.ppt"])
        form.lot_id = lot
        self.assertEqual(form.product_id3, self.ppt)
        form.product_id3 = self.pts
        self.assertFalse(form.lot_id)

    def test_migration_integer_serial(self):
        cr = self.env.cr
        cr.execute(
            "CREATE TEMP TABLE lat_test_int ("
            " id serial, product_id2 integer, num_serie2 integer, lot_id integer)"
        )
        cr.execute(
            "INSERT INTO lat_test_int (product_id2, num_serie2) VALUES"
            " (%(p)s, 265709), (%(p)s, 0), (NULL, 265710)",
            {"p": self.pts.id},
        )
        serial_to_lot(cr, "lat_test_int", "num_serie2", "product_id2")
        cr.execute(
            "SELECT l.name FROM lat_test_int t"
            " LEFT JOIN stock_lot l ON l.id = t.lot_id ORDER BY t.id"
        )
        self.assertEqual([row[0] for row in cr.fetchall()], ["265709", None, None])
