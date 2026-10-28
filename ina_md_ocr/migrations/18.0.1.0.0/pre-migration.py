# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    cr.execute(
        """
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'inael_ocr' AND column_name = 'proyecto_id'
        """
    )
    if cr.fetchone():
        cr.execute(
            "ALTER TABLE inael_ocr RENAME COLUMN proyecto_id TO proyecto_legacy_id"
        )
