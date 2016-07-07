# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Rockbotic - Custom",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "product",
        "purchase",
        "crm",
        "sale_order_create_event",
        "sale_order_line_performance",
        "sale_service_recurrence_configurator",
        "event_planned_by_sale_line",
        "event_report",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/crm_lead_view.xml",
        "views/res_partner_view.xml",
        "views/product_category_view.xml",
        "report/rockbotic_custom_view.xml",
        "report/rockbotic_reports.xml",
    ],
    "installable": True,
}
