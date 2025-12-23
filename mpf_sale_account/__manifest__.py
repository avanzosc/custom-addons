# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Mpf Sale Account",
    "version": "18.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": ["account", "sale_crm", "mpf_general"],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_sale_lead_in_account_invoice",
}
