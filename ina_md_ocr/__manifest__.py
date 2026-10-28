# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Inael Gestion de OCRs",
    "version": "18.0.1.0.0",
    "summary": "Gestion de OCRs de Iberdrola",
    "category": "Inael md",
    "license": "AGPL-3",
    "author": "Inael, jag",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "mrp",
        "ina_mc_permisos",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/inael_ocr_view.xml",
        "views/inael_ocr_line_view.xml",
        "views/inael_ocr_menu.xml",
    ],
    "installable": True,
}
