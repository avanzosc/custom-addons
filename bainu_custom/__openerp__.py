# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Bainu - Custom",
    "version": "8.0.1.3.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <ajuaristio@gmail.com>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "account_voucher",
        "sale_order_dates",
        "sale_crm",
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/sale_order_view.xml",
        "report/invoice_reports.xml",
        "report/sale_order_report.xml",
    ],
    "installable": True,
}
