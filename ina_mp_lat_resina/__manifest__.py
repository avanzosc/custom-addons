# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina Mp Lat Resina",
    "version": "18.0.1.0.0",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "INAEL,jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "mrp",
        "ina_mc_permisos",
        "ina_mp_lat_res_ensayos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/lat_res_inyeccion.xml",
        "views/lat_res_pts.xml",
        "views/lat_res_ppt.xml",
        "views/lat_res_mezcla.xml",
        "views/stock_lot_views.xml",
    ],
    "installable": True,
}
