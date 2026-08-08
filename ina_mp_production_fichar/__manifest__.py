# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina MP Production Fichar",
    "version": "18.0.1.0.0",
    "category": "Inael MP",
    "license": "AGPL-3",
    "author": "INAEL, jag, AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "mrp",
        "hr_attendance",
        "stock",
        "ina_mc_permisos",
        "ina_mc_product_campos",
        "ina_mp_mrp_repara",
        "ina_mp_production_olaser",
        "mrp_productivity_employee",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_puesto_fichar_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_employee_fichar_views.xml",
        "views/stock_scrap_views.xml",
        "views/stock_move_views.xml",
        "wizard/wiz_fichar_orden.xml",
    ],
    "installable": True,
}
