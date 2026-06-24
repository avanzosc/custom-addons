# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina Mrp production Olaser",
    "version": "18.0.1.0.0",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "Inael, jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "stock",
        "ina_mc_permisos",
        "ina_mc_product_campos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/order_olaser.xml",
        "views/olaser_tiempos.xml",
        "views/olaser_lista.xml",
        "wizard/wiz_listar_olaser.xml",
        "data/code_sequence.xml",
    ],
    "installable": True,
}
