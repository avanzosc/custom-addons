# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Igalia - Custom",
    "summary": "",
    "version": "8.0.1.1.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Mikel Urbistondo <mikelurbistondo@avanzosc.es>",
    ],
    "depends": [
        "product",
        "account",
        "report",
        "sale",
        "account_invoice_pricelist",
        "hr_timesheet_invoice",
        "account_asset",
    ],
    "data": [
        "views/igalia_layout_view.xml",
        "views/product_view.xml",
        "views/igalia_report_view.xml",
        "views/igalia_custom_view.xml",
        "views/account_analytic_view.xml",
        "views/account_invoice_view.xml",
        "views/account_asset_asset_view.xml",
        "views/asset_asset_report_view.xml",
    ],
    "installable": True,
}
