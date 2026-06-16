# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Drcol Reports",
    "version": "18.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "account",
        "account_payment_partner",
        "account_payment_sale",
        "sale",
        "stock",
        "sale_stock",
        "stock_delivery",
        "web",
        "drcol_custom",
    ],
    "data": [
        "report/report_layouts.xml",
        "report/invoice_report.xml",
        "report/sale_order_report.xml",
        "report/stock_picking_report.xml",
    ],
    "installable": True,
}
