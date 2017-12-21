# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    @api.multi
    def check(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id', False)
        order = self.env['pos.order'].browse(active_id)
        order.action_truke()
        return super(PosMakePayment, self).check()
