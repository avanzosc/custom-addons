# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Astikar - Custom",
    "summary": "",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es",
    ],
    "depends": [
        "mrp_repair",
        "mrp_repair_fee",
        "mrp_repair_date",
        "web",
        "report",
        "mrp_repair_proforma_report",
        "account_payment_partner",
    ],
    "data": [
        "views/astikar_custom_view.xml",
        "views/astikar_layout_view.xml",
        "views/astikar_reports.xml",
    ],
    "installable": True,
}
