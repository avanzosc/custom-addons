# -*- coding: utf-8 -*-
# © 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Tumaker Picking Report",
    "version": "8.0.1.2.0",
    "license": "AGPL-3",
    "depends": [
        "stock_valued_picking_report",
        "mrp_bom_sale_pack",
        "report_gdpr"
        ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Reporting",
    'data': [
        "views/valued_stock_picking_report.xml",
        "views/report_stock_picking.xml",
        ],
    'installable': True,
}
