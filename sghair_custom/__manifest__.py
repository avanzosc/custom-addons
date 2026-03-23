# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Sghair Custom",
    "version": "18.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "account_payment_partner",
        "sale_management",
        "purchase",
        "sales_team",
        "stock",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/report_templates.xml",
        "views/account_invoice_view.xml",
        "views/purchase_order_view.xml",
        "views/res_company_logo_view.xml",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
