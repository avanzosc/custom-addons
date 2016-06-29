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
        "sale_order_create_event",
        "report",
    ],
    "data": [
        "views/sale_order_view.xml",
        "report/rockbotic_custom_view.xml",
        "report/rockbotic_reports.xml",
    ],
    "installable": True,
}
