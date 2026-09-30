# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase

from odoo.addons.ina_mp_lat_res_ensayos.lat_lot_migration import serial_to_lot


class TestLatLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Pararrayos LAT", "is_storable": True}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Trafo LAT", "is_storable": True}
        )

    def _lot(self, name, product=None):
        return self.env["stock.lot"].create(
            {"name": name, "product_id": (product or self.product).id}
        )

    def test_lot_sets_product_tracking(self):
        lot = self._lot("261000001")
        ensayo = self.env["res.pararrayos"].create(
            {"name": 261000001, "product_id": self.product.id, "lot_id": lot.id}
        )
        self.assertEqual(self.product.tracking, "serial")
        self.assertEqual(lot.lat_pararrayos_ids, ensayo)

    def test_equipo_lot_tracking(self):
        equipo = self.env["product.product"].create(
            {"name": "Cargador bateria", "is_storable": True}
        )
        lot = self._lot("26002369/088", equipo)
        linea = self.env["res.celdas.equipos"].create(
            {"product_id": equipo.id, "lot_id": lot.id}
        )
        self.assertEqual(equipo.tracking, "lot")
        self.assertEqual(lot.lat_celdas_equipo_ids, linea)
        self.product.tracking = "serial"
        self.env["res.celdas.equipos"].create(
            {"product_id": self.product.id, "lot_id": self._lot("13059").id}
        )
        self.assertEqual(self.product.tracking, "serial")

    def test_conexion_lot_shared_by_celdas(self):
        pasatapas = self.env["product.product"].create(
            {"name": "Pasatapas", "is_storable": True}
        )
        lot = self._lot("1683", pasatapas)
        celdas = self.env["res.celdas"].create([{"name": 40143}, {"name": 42235}])
        conexiones = self.env["res.celdas.conexiones"].create(
            [
                {"celda_id": celda.id, "product_id": pasatapas.id, "lot_id": lot.id}
                for celda in celdas
            ]
        )
        self.assertEqual(pasatapas.tracking, "lot")
        self.assertEqual(lot.lat_celdas_conexion_ids, conexiones)
        self.assertEqual(lot.lat_celdas_conexion_ids.celda_id, celdas)

    def test_lot_of_other_product(self):
        lot = self._lot("261000002", self.other_product)
        with self.assertRaises(ValidationError):
            self.env["res.pararrayos"].create(
                {"product_id": self.product.id, "lot_id": lot.id}
            )

    def test_duplicate_trafo_creates_lot(self):
        trafo = self.env["res.trafos"].create(
            {
                "name": 2607001,
                "product_id": self.other_product.id,
                "lot_id": self._lot("2607001", self.other_product).id,
            }
        )
        self.env["wiz.trafos.duplicar"].with_context(active_ids=trafo.ids).create(
            {"num_serie": 2607002}
        ).action_duplica_trafo()
        copia = self.env["res.trafos"].search([("name", "=", 2607002)])
        self.assertEqual(copia.lot_id.name, "2607002")
        self.assertEqual(copia.lot_id.product_id, self.other_product)

    def test_migration_serial_to_lot(self):
        cr = self.env.cr
        cr.execute(
            """
            CREATE TEMP TABLE lat_test (
                id serial, product_id integer, num_serie numeric, lot_id integer)
            """
        )
        cr.execute(
            """
            INSERT INTO lat_test (product_id, num_serie) VALUES
                (%(p)s, 261000003), (%(p)s, 261000003.0), (%(p)s, 0), (NULL, 261000004)
            """,
            {"p": self.product.id},
        )
        product_ids = serial_to_lot(cr, "lat_test", "num_serie")
        self.assertEqual(product_ids, {self.product.id})
        cr.execute("SELECT num_serie, lot_id FROM lat_test ORDER BY id")
        rows = cr.fetchall()
        lot = self.env["stock.lot"].browse(rows[0][1])
        self.assertEqual(lot.name, "261000003")
        self.assertEqual(rows[1][1], lot.id)
        self.assertEqual([row[1] for row in rows[2:]], [None, None])

    def test_migration_keeps_any_text(self):
        cr = self.env.cr
        cr.execute(
            "CREATE TEMP TABLE lat_test_char ("
            " id serial, product_id integer, num_serie varchar, lot_id integer)"
        )
        cr.execute(
            "INSERT INTO lat_test_char (product_id, num_serie) VALUES"
            " (%(p)s, ' 001 '), (%(p)s, '000'), (%(p)s, 'XXXX'), (%(p)s, '  ')",
            {"p": self.product.id},
        )
        serial_to_lot(cr, "lat_test_char", "num_serie")
        cr.execute(
            "SELECT l.name FROM lat_test_char t"
            " LEFT JOIN stock_lot l ON l.id = t.lot_id ORDER BY t.id"
        )
        self.assertEqual(
            [row[0] for row in cr.fetchall()], ["001", "000", "XXXX", None]
        )
