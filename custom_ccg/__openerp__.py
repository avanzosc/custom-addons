# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Custom CCG",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "product",
        "mrp",
        "mrp_production_sale_info",
    ],
    "category": "Manufacturing",
    "data": [
        "views/mrp_production_view.xml",
        "views/product_packaging_view.xml",
    ],
    "installable": True
}
