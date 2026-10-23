# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Inael Gestion de Fichajes - Produccion",
    "version": "18.0.1.0.0",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "INAEL,jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "hr",
        "mrp",
        "repair",
        "mrp_laser_cut",
        "ina_mc_permisos",
        "ina_mc_product_campos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_views.xml",
        "views/hr_employee_fichar_views.xml",
        "views/hr_puesto_fichar_views.xml",
        "views/product_product_views.xml",
        "views/stock_move_views.xml",
        "views/stock_scrap_views.xml",
        "views/stock_location_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
}
