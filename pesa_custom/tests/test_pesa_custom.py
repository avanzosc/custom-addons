# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from datetime import datetime, date
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestPesaCustom(common.TransactionCase):

    def setUp(self):
        super(TestPesaCustom, self).setUp()
        self.schedule_model = self.env['schedule']
        self.crm_claim = self.env.ref('crm_claim.crm_claim_1')
        self.company = self.ref('base.main_company')
        self.crm_claim2 = self.env.ref('crm_claim.crm_claim_2')
        self.phonecall_model = self.env['crm.phonecall']

    def test_name_search(self):
        self.schedule1 = self.schedule_model.create({'hour': 16.5})
        res = self.schedule1.name_get()
        self.assertEqual([x[1] for x in res][0], '16:30',
                         'Schedule is not the same')

    def test_compute_calendar_date(self):
        self.crm_claim.date_deadline = date.today().replace(month=3, day=15)
        self.assertEqual(
            self.crm_claim.calendar_date, self.crm_claim.date_deadline)
        self.crm_claim.date_action_next = datetime.now().replace(day=20)
        date_format = datetime.strptime(self.crm_claim.date_action_next,
                                        '%Y-%m-%d %H:%M:%S')
        self.assertEqual(self.crm_claim.calendar_date,
                         date_format.date().strftime("%Y-%m-%d"))

    def test_onchange_company_id(self):
        schedule = self.schedule_model.create({
            'hour': 8.5,
            'company_id': self.company})
        self.crm_claim.company_id = self.company
        res = self.crm_claim.onchange_company_id()
        schedule_res = self.schedule_model.search(
            (res['domain']['schedule_id']))
        self.assertEqual(schedule, schedule_res)

    def test_compute_priority(self):
        self.crm_claim.to_related_claims = [(4, self.crm_claim2.id, 0)]
        self.assertEqual(self.crm_claim2.priority, '4')
        self.assertEqual(self.crm_claim.priority, '1')

    def test_hang_up_call(self):
        phonecall = self.phonecall_model.create({'name': 'Test'})
        phonecall.make_call()
        now = fields.Datetime.now()
        self.assertEqual(phonecall.date_open, now)
        phonecall.date_open = \
            fields.Datetime.from_string(phonecall.date_open) - \
            relativedelta(seconds=30)
        view = phonecall.hang_up_call()
        self.assertEqual(
            view['view_id'], self.ref('crm.crm_case_phone_form_view'))
        self.assertEqual(phonecall.duration, 0.5)
