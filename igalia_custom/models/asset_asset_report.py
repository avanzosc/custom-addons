# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, tools


class AssetAssetReport(models.Model):
    _inherit = 'asset.asset.report'

    active = fields.Boolean(string="Active", readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'asset_asset_report')
        cr.execute("""
            create or replace view asset_asset_report as (
                select
                    min(dl.id) as id,
                    dl.name as name,
                    dl.depreciation_date as depreciation_date,
                    a.purchase_date as purchase_date,
                    (CASE WHEN dlmin.id = min(dl.id)
                      THEN a.purchase_value
                      ELSE 0
                      END) as gross_value,
                    dl.amount as depreciation_value,
                    (CASE WHEN dl.move_check
                      THEN dl.amount
                      ELSE 0
                      END) as posted_value,
                    (CASE WHEN NOT dl.move_check
                      THEN dl.amount
                      ELSE 0
                      END) as unposted_value,
                    dl.asset_id as asset_id,
                    dl.move_check as move_check,
                    a.category_id as asset_category_id,
                    a.partner_id as partner_id,
                    a.state as state,
                    count(dl.*) as nbr,
                    a.company_id as company_id,
                    a.active as active
                from account_asset_depreciation_line dl
                    left join account_asset_asset a on (dl.asset_id=a.id)
                    left join (select min(d.id) as id,
                    ac.id as ac_id from account_asset_depreciation_line as
                    d inner join account_asset_asset as ac ON
                    (ac.id=d.asset_id) group by ac_id)
                     as dlmin on dlmin.ac_id=a.id
                group by
                    dl.amount,dl.asset_id,dl.depreciation_date,dl.name,
                    a.purchase_date, dl.move_check, a.state, a.category_id,
                     a.partner_id, a.company_id,
                    a.active, a.purchase_value, a.id, a.salvage_value,
                     dlmin.id)""")
