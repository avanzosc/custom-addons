# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina Mp Ensayos Lat",
    "version": "18.0.1.0.0",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "INAEL,jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "product",
        "mrp",
        "ina_mc_permisos",
        "ina_mp_lat_res_ensayos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_ensayos_view.xml",
        "views/mrp_ensayos_producto_view.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "wizard/wiz_ensayos_duplica.xml",
    ],
    "installable": True,
}
