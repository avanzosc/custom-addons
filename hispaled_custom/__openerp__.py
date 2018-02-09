# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Hispaled",
    "summary": "Customization Module",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "mrp",
        "mrp_label_print",
        "mrp_unitary_production",
        "product_variant_default_code",
        "stock_picking_label_print",
    ],
    "data": [
        "views/mrp_production_views.xml",
        "views/stock_label_report.xml",
        "views/stock_label_report_data_views.xml",
        "wizard/mrp_product_produce_views.xml",
    ],
    "installable": True,
}
