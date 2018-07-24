# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Urbistondo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class AssetAssetReport(models.Model):
    _inherit = 'asset.asset.report'

    active = fields.Boolean(
        related='asset_id.active', string="Active", readonly=True)
