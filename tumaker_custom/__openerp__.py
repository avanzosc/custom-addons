# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Tumaker custom",
    "version": "8.0.2.0.0",
    "license": "AGPL-3",
    "depends": ["sale_order_dates",
                "project_timesheet",
                "sale_service",
                "account_analytic_analysis",
                "product_analytic",
                "purchase_discount",
                "stock",
                "account_invoice_line_lot",
                "account_payment_partner",
                "delivery",
                "stock_valued_picking_report",
                "warning",
                "product_pricelist_rules",
                "account_due_list",
                "sale_crm",
                "mrp",
                "contacts",
                "marketing",
                "web_context_tunnel",
                ],
    "author": "Avanzosc, S.L.",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "category": "Custom Module",
    "website": "http://www.avanzosc.es",
    "complexity": "easy",
    "data": ['security/res_groups.xml',
             'security/ir.model.access.csv',
             'data/cron_data.xml',
             'views/sale_order_view.xml',
             'views/account_analytic_account_view.xml',
             'views/timesheet_sheet_view.xml',
             'views/project_view.xml',
             'views/report_contract_summary.xml',
             'views/purchase_order_view.xml',
             'views/report_basque.xml',
             'views/stock_picking_view.xml',
             'views/stock_quant_view.xml',
             'views/account_invoice_view.xml',
             'views/res_company_view.xml',
             'views/product_view.xml',
             'views/account_move_line_view.xml',
             'views/report_purchase_order.xml',
             'views/res_partner_view.xml',
             'views/crm_lead_view.xml',
             'views/specific_stock_production_menuitem.xml',
             'wizard/stock_transfer_details_view.xml',
             'wizard/crm_make_sale_view.xml',
             'report/account_entries_report_view.xml'
             ],
    "installable": True,
    "auto_install": False,
}
