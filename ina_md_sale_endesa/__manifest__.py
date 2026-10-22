# © 2016 Eficent Business and IT Consulting Services S.L.
#   (<http://www.eficent.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Entegas de OV de Endesa",
    "version": "18.0.1.0.0",
    "category": "Inael md",
    "license": "AGPL-3",
    "author": "Inael, jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "sale",
        "ina_mc_permisos",
        "ina_mp_product_homologaciones",
        "web_tree_dynamic_colored_field",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/inael_endesa_view.xml",
    ],
    "installable": True,
}
