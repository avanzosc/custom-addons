# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Galaxia - Custom",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "analytic",
        "account_analytic_analysis",
        "account_payment_partner",
        "event",
        "sale_mrp",
        "sale_product_variants",
        "sale_stock_product_variants",
        "product_variants_types",
        "sale_order_line_attached_check",
        "sale_order_line_performance",
        "sale_service_recurrence_configurator",
        "sale_order_line_service_view",
        "website_quote_not_unlink",
        "sale_order_create_event",
        "product",
        "project",
        "stock",
        "account_voucher",
        "quality_control_mrp",
        "quality_control_stock",
    ],
    "data": [
        "data/request_link_data.xml",
        "views/product_view.xml",
        "views/event_view.xml",
        "views/account_analytic_view.xml",
        "views/sale_order_view.xml",
        "views/account_view.xml",
        "report/galaxia_custom_view.xml",
        "report/galaxia_layout_view.xml",
        "report/galaxia_reports.xml",
    ],
    "installable": True,
}
