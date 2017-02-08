# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "DS - Custom",
    "summary": "",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
    ],
    "depends": [
        "base", "crm_partner_assign", "portal", "portal_sale", "website",
        "stock", "purchase",
    ],
    "data": [
        "security/ds_portal_security.xml",
        'security/ir.model.access.csv',
        "views/ds_custom_css.xml",
        "views/portal_view.xml",
        "views/ds_custom_web_view.xml",
        "views/ds_custom_picking_report.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
