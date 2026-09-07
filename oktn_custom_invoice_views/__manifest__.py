# Copyright 2019 Alejandro Nieto - Okatent
# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Oktn Custom Invoice Views",
    "version": "18.0.1.1.0",
    "category": "Accounting/Accounting",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "account",
        "sale_project",
        "l10n_es_aeat_sii_oca",
    ],
    "data": [
        "views/account_invoice_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
}
