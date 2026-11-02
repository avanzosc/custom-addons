# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Ina MP MRP Repara",
    "version": "18.0.1.0.0",
    "summary": "Gestión de reparaciones: estados, materiales, tiempos, documentación",
    "category": "Inael mp",
    "license": "AGPL-3",
    "author": "INAEL, jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "repair",
        "crm_claim_links",
        "mrp",
        "hr",
        "ina_mc_permisos",
        "ina_mc_product_campos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/repair_order_views.xml",
        "views/mrp_repair_tiempos_views.xml",
        "wizard/docu_rma_ver.xml",
    ],
    "installable": True,
}
