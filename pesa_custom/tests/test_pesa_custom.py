# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from datetime import datetime, date


class TestPesaCustom(common.TransactionCase):

    def setUp(self):
        super(TestPesaCustom, self).setUp()
        self.schedule_model = self.env['schedule']
        self.journey_model = self.env['journey']
        self.real_line_model = self.env['real.line']

    def test_name_search(self):
        self.schedule1 = self.schedule_model.create({'hour': 16.5})
        res = self.schedule1.name_get()
        self.assertEqual([x[1] for x in res][0], '16:30',
                         'Schedule is not the same')

    def test_compute_calendar_date(self):
        crm_claim = self.env.ref('crm_claim.crm_claim_1')
        crm_claim.date_deadline = date.today().replace(month=3, day=15)
        self.assertEqual(crm_claim.calendar_date, crm_claim.date_deadline)
        crm_claim.date_action_next = datetime.now().replace(day=20)
        date_format = datetime.strptime(crm_claim.date_action_next,
                                        '%Y-%m-%d %H:%M:%S')
        self.assertEqual(crm_claim.calendar_date,
                         date_format.date().strftime("%Y-%m-%d"))
