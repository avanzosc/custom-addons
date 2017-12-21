# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Trukebai",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC, Odoo Community Association (OCA)",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "stock_account",
        "sale_stock",
        "point_of_sale"
    ],
    "data": [
        "data/product_data.xml",
        "data/paperformat_data.xml",
        "data/trukebai_data.xml",
        "security/ir.model.access.csv",
        "wizard/stock_transfer_details_view.xml",
        "views/stock_picking_view.xml",
        "views/res_partner_view.xml",
        "views/report_product_label.xml",
        "views/report_product_product_label.xml",
        "views/report_picking_receipt.xml",
        "views/report_view.xml",
        "views/product_product_view.xml",
        "views/sale_order_view.xml",
        "views/pos_order_view.xml",
        "views/trukebai_saleswoman_view.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
}
