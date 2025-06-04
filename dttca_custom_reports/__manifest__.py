# 2018 Alquemy - Javier de las Heras <jheras@alquemy.es>
# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Dietetica Custom Reports",
    "version": "16.0.1.0.0",
    "author": "Alquemy & AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "license": "AGPL-3",
    "category": "Custom",
    "depends": [
        "base",
        "sale",
        "stock",
        "purchase",
        "purchase_stock",
        "account",
        "web",
        "stock_picking_invoice_link",
        "product_expiry",
        "delivery_package_number",
        "l10n_es_aeat_mod347",
        "product_recommended_price",
        "account_payment_partner",
        "account_banking_mandate"
    ],
    "data": [
        "report/paperformat.xml",
        "report/reports.xml",
        "report/report_layouts_alq.xml",
        "report/report_layouts_empty_alq.xml",
        "report/report_347_partner.xml",
        "report/report_account_invoice_alq.xml",
        "report/report_picking_alq.xml",
        "report/report_sale_order_alq.xml",
        "report/stock_label_template.xml",
#        "report/report_sale_order_without_prices_alq.xml",
        "report/report_purchase_order.xml",
        "report/report_purchase_quotation.xml",
    ],
    "installable": True,
}
