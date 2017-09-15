# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def delete_columns(cr):
    cr.execute(
        """
        ALTER TABLE stock_move DROP COLUMN IF EXISTS sale_price_unit;
        ALTER TABLE stock_move DROP COLUMN IF EXISTS sale_price_discount;
        ALTER TABLE stock_move DROP COLUMN IF EXISTS sale_price_subtotal;
        """)


def migrate(cr, version):
    if not version:
        return
    delete_columns(cr)
