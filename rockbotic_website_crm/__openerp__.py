# -*- coding: utf-8 -*-
# Copyright © 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Rockbotic - Website CRM",
    "version": "8.0.2.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "website",
        "website_crm_address",
        "crm_lead_to_event_registration",
        "event_track_assistant",
        "event_registration_analytic",
        "partner_contact_birthdate",
        "partner_prospect",
        "partner_parent_change",
        "base_iban",
        "l10n_es_partner",
        "account_banking_sepa_direct_debit",
        "rockbotic_custom",
    ],
    "data": [
        "data/rockbotic_website_crm_data.xml",
        "security/rockbotic_website_crm.xml",
        "wizard/res_partner_enroll_search_view.xml",
        "wizard/crm_lead_to_opportunity_view.xml",
        "views/res_partner_view.xml",
        # "views/contactus_form.xml",
        "views/crm_lead_view.xml",
        "views/website_crm.xml",
        "views/res_company_view.xml",
        "views/event_event_view.xml",
    ],
    "installable": True,
}
