# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, exceptions, api, _


class StockTransferDetails(models.TransientModel):

    _inherit = 'stock.transfer_details'

    allow_zero_cost = fields.Boolean(string="Allow Zero Costs")

    @api.multi
    def do_detailed_transfer(self):
        lines_zero_cost = self.picking_id.move_lines.filtered(
            lambda x: x.price_unit == 0 and x.state != 'cancel')
        if self.picking_id.picking_type_code == 'incoming' and \
                lines_zero_cost and not self.allow_zero_cost:
            raise exceptions.Warning(_('You have some lines without costs.'))
        return super(StockTransferDetails, self).do_detailed_transfer()
