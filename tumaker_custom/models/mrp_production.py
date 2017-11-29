# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class MrpProduction(models.Model):

    _inherit = "mrp.production"

    @api.onchange('routing_id')
    @api.multi
    def onchange_routing_id(self):
        self.ensure_one()
        if self.routing_id.location_id:
            self.location_src_id = self.routing_id.location_id
            self.location_dest_id = self.routing_id.location_id
