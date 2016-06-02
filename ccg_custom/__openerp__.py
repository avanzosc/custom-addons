# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "CCG Custom",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "procurement",
        "mrp",
        "sale",
        "sale_order_dates",
    ],
    "category": "Custom Module",
    "data": [
        "views/mrp_production_view.xml",
        "views/product_packaging_view.xml",
        "views/sale_order_view.xml",
        "views/account_invoice_view.xml",
    ],
    "installable": True
}
