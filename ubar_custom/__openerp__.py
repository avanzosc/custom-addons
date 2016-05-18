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
        "report",
        "account_payment_partner",
        "stock",
        "website_quote",
        "sale_order_dates",
        "purchase_discount",
        "delivery",
        "stock_valued_picking_report",
        "sale_order_due_date",
        "purchase_product_menu",
        "sale_order_type",
        "purchase_order_line_view",
        "sale_order_line_view",
        "mrp",
    ],
    "category": "Custom Modules",
    "data": [
        "security/ir.model.access.csv",
        "views/machinery_view.xml",
        "views/product_view.xml",
        "views/product_move_view.xml",
        "views/sale_order_view.xml",
        "views/stock_view.xml",
        "views/analytic_account_view.xml",
        "views/purchase_order_view.xml",
        "reports/ubar_layout_view.xml",
        "reports/ubar_reports.xml",
        "reports/ubar_paperformat.xml",
    ],
    "installable": True,
}
