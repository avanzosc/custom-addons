# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Mot Product Ean Automatic",
    "version": "18.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "category": "Sales/Sales",
    "depends": ["base", "base_setup", "mail", "product", "stock"],
    "data": [
        "security/product_security.xml",
        "data/email_ean_code.xml",
        "view/res_config.xml",
        "view/product_template.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
