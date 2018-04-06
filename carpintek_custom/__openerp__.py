# -*- coding: utf-8 -*-
# Copyright (c) 2018  Daniel Campos - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Carpintek custom",
    "version": "8.0.1.0.0",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Daniel Campos <danielcampos@avanzosc.es>",
    ],
    "depends": ['account', 'purchase', 'sale',
                ],
    "category": "Custom Modules",
    "data": ['views/account_invoice_view.xml',
             'views/purchase_view.xml',
             'views/sale_view.xml',
             ],
    "installable": True
}
