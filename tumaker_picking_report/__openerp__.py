# -*- coding: utf-8 -*-
# © 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Tumaker Picking Report",
    "version": "8.0.1.0.0",
    "depends": ["stock_valued_picking_report"],
    "author": "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "http://www.odoomrp.com",
    "category": "Reporting",
    "description": """
        Little changes on picking report for Tumaker.
        - Description of move replaces product name.
    """,
    'data': ["views/valued_stock_picking_report.xml",
             "views/report_stock_picking.xml"],
    'installable': True,
}
