# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Website CRM Rockbotic",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Lets visitors fill in their address in the contact form",
    "depends": [
        'website_crm_address',
        'event_registration_analytic',
        'partner_contact_birthdate',
    ],
    "data": [
        "views/contactus_form.xml",
        "views/crm_lead_view.xml",
    ],
    "installable": True,
}
