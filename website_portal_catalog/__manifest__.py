# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Portal Catalog",
    "version": "18.0.2.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/custom-addons",
    "category": "Tools",
    "depends": [
        "acysos_hlc",
        "report_xlsx",
        "sale",
        "sale_report_product_attributes",
        "website_sale",
    ],
    "data": [
        "data/catalog_data.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/website_catalog_template.xml",
        "views/product_catalog_ftp_views.xml",
        "reports/reports.xml",
    ],
    "installable": True,
}
