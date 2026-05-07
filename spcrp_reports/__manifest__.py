# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Spcrp Reports",
    "version": "18.0.1.0.0",
    "category": "Custom",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "account",
        "sale",
        "sale_stock",
        "sale_order_line_sequence",
        "product_make",
    ],
    "data": [
        "reports/external_layout.xml",
        "reports/report_invoice.xml",
        "reports/report_sale.xml",
    ],
    "installable": True,
}
