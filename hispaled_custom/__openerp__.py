# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Hispaled",
    "summary": "Customization Module",
    "version": "8.0.1.2.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "mrp",
        "mrp_label_print",
        "mrp_unitary_production",
        "product_attribute_code_field",
        "product_variant_default_code",
        "stock_picking_label_print",
        "account_payment_purchase",
        "sale_proforma_report",
        "sale_stock",
        "product_variants_no_automatic_creation",
        "account_invoice_line_stock_move_info",
        "product_variant_description"
    ],
    "data": [
        "views/mrp_production_views.xml",
        "views/stock_label_report.xml",
        "views/stock_label_report_data_views.xml",
        "views/stock_picking_views.xml",
        "views/res_company_views.xml",
        "views/account_invoice_views.xml",
        "wizard/mrp_product_produce_views.xml",
        "data/report_paperformat.xml",
        "report/purchase_order_report.xml",
        "report/stock_picking_report.xml",
        "report/sale_order_report.xml",
        "report/account_invoice_report.xml",
    ],
    "installable": True,
}
