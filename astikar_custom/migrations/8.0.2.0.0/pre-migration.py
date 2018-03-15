# -*- coding: utf-8 -*-
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.htm


def update_manual_purchase_info(cr):
    cr.execute("""
        ALTER TABLE product_product ADD COLUMN manual_purchase_date date;
    """)
    cr.execute("""
        UPDATE product_product SET manual_purchase_date = last_purchase_date;
    """)
    cr.execute("""
        ALTER TABLE product_product ADD COLUMN manual_supplier_id integer;
    """)
    cr.execute("""
        UPDATE product_product SET manual_supplier_id = last_supplier_id;
    """)
    cr.execute("""
        ALTER TABLE product_product ADD COLUMN manual_purchase_price numeric;
    """)
    cr.execute("""
        UPDATE product_product SET manual_purchase_price = last_purchase_price;
    """)


def migrate(cr, version):
    if not version:
        return
    update_manual_purchase_info(cr)
