# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Tumaker CRM custom',
    'version': '11.0.1.0.0',
    'depends': [
        'base',
        'sales_team',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Tumaker CRM custom''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'security/partner_security.xml',
        ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
}
