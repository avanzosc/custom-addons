# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class EventTrackPresenceReport(models.Model):
    _inherit = "event.track.presence.report"

    def _from(self):
        from_str = """
        from   event_track_presence p
               inner join event_event e on e.id = p.event
               inner join account_analytic_account a on a.sale = e.sale_order
               inner join res_partner r on r.id = a.agreement_address
        """
        return from_str
