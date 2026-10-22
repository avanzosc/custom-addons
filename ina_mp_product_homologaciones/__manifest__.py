# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Homologaciones de productos.",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "Inael, jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "sale",
        "mrp",
        "ina_mc_permisos",
        "ina_mc_product_campos",
    ],
    "data": [
        "security/ina_mp_product_homologaciones_security.xml",
        "security/ir.model.access.csv",
        "views/mrp_homologa_view.xml",
        "views/product_cia_view.xml",
        "views/product_view.xml",
    ],
    "installable": True,
}
