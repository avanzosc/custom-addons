# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    _order = "inventory_id, location_name, product_name, prodlot_name"
