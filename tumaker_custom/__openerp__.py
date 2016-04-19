# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Tumaker custom",
    "version": "1.0",
    "depends": ["sale_order_dates",
                "project_timesheet",
                "sale_service",
                "account_analytic_analysis",
                "product_analytic",
                "purchase",
                "stock",
                "account_invoice_line_lot",
                "account_payment_partner",
                "delivery",
                ],
    "author": "Avanzosc, S.L.",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "category": "Custom Module",
    "website": "http://www.avanzosc.es",
    "complexity": "easy",
    "data": ['views/sale_order_view.xml',
             'views/account_analytic_account_view.xml',
             'views/timesheet_sheet_view.xml',
             'views/project_view.xml',
             'views/report_contract_summary.xml',
             'views/purchase_order_view.xml',
             'views/report_basque.xml',],
    "installable": True,
    "auto_install": False,
}
