# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Ubar Custom",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Daniel Campos <danielcampos@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "machine_manager",
        "sale",
    ],
    "category": "Custom Modules",
    "data": [
        "views/machinery_view.xml",
        "views/product_view.xml",
        "views/product_move_view.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
