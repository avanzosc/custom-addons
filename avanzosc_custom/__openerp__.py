# -*- coding: utf-8 -*-
# (c) 2015 Serv. Tecnol. Avanzados - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Avanzosc custom modifications',
    'version': '8.0.2.0.0',
    'category': 'Custom modifications',
    'author': 'Serv. Tecnol. Avanzados - Pedro M. Baeza',
    'website': 'http://www.serviciosbaeza.com',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'crm_claim',
    ],
    'data': [
        'data/crm_claim_data.xml',
        'views/sale_order_view.xml',
        'views/crm_claim_view.xml',
    ],
    "installable": True,
}
