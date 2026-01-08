# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "MPF Crm",
    "summary": "Personalizaciones Odoo para MP Fluids",
    "version": "18.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": ["sale", "crm", "sale_crm", "sales_team", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_belong_views.xml",
        "views/crm_lead_brand_views.xml",
        "views/crm_lead_type_views.xml",
        "views/crm_lead_views.xml",
        "views/account_move_views.xml",
    ],
    "post_init_hook": "_post_install_put_sale_lead_in_account_invoice",
}
