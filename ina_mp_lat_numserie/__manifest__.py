# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina Mp Lat Numserie",
    "version": "18.0.1.0.0",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "INAEL,jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "ina_mp_lat_res_ensayos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/lat_num_views.xml",
        "views/lat_numserie_views.xml",
        "views/lat_numcentro_views.xml",
        "views/lat_numcentro_lineas_views.xml",
        "wizard/wiz_informe_centro_views.xml",
    ],
    "installable": True,
}
