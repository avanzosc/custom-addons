# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Lx Reports",
    "version": "18.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "web",
        "stock",
        "delivery",
        "stock_delivery",
        "sale",
        "account",
        "account_invoice_weight",
        "res_company_signature_fields",
        "res_partner_eori_number",
        "sale_order_line_date",
        "sale_management",
        "purchase",
    ],
    "data": [
        "reports/external_layout_standard_templates.xml",
        "reports/report_delivery_document_inherit.xml",
        "reports/account_invoice_report.xml",
        "reports/sale_order_report.xml",
        "reports/purchase_order_report.xml",
    ],
}
