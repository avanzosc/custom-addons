# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestRockboticCustom(common.TransactionCase):

    def setUp(self):
        super(TestRockboticCustom, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.invoice_model = self.env['account.invoice']
        self.ir_values_obj = self.env['ir.values']
        self.partner_model = self.env['res.partner']
        self.holiday_model = self.env['hr.holidays']
        self.contract_model = self.env['hr.contract']
        self.wiz_workable_model = self.env['wiz.calculate.workable.festive']
        self.message_model = self.env['mail.message']
        self.email_model = self.env['wiz.send.email.registration.evaluation']
        self.email2_model = self.env['wiz.send.email.event.evaluation']
        self.attachment_model = self.env['ir.attachment']
        self.partner = self.browse_ref('base.res_partner_address_20')
        self.parent = self.partner.parent_id
        claim_vals = {'name': 'Rockbotic test',
                      'partner_id': self.partner.id}
        self.claim = self.claim_model.create(claim_vals)
        self.contract = self.env.ref('account.analytic_support_internal')
        self.contract.recurring_invoices = True
        self.comment = u'Testing ir value'
        self.ir_values_obj.set_default(
            'account.invoice', 'comment', self.comment)
        event_vals = {'name': 'test rockbotic_custom',
                      'date_begin': '2025-01-20 15:00:00',
                      'date_end': '2025-01-30 16:00:00'}
        self.event = self.env['event.event'].create(event_vals)
        registration_vals = {'event_id': self.event.id,
                             'partner_id': self.partner.id}
        self.registration = self.env['event.registration'].create(
            registration_vals)

    def test_rockbotic_custom(self):
        self.assertEqual(self.partner.claim_count, 1,
                         'Bad number of claims for partner')
        res = self.partner.show_crm_claims_from_partner()
        domain = "[('id', 'in', [{}])]".format(self.claim.id)
        self.assertNotIn(domain, res.get('domain', False),
                         'Bad domain in show_crm_claims_from_partner')

    def test_analytic_recurring(self):
        self.contract.recurring_create_invoice()
        invoice = self.invoice_model.search([
            ('origin', '=', self.contract.code)])
        self.assertEqual(invoice.comment, self.comment)

    def test_send_email(self):
        self.parent.write({'email': 'test@test.com',
                           'notify_email': 'none'})
        self.event._send_email_to_registrations('email body')
        self.parent.email = False
        with self.assertRaises(exceptions.Warning):
            self.event._validate_registrations_email()
        self.env.ref(
            'event_registration_mass_mailing.email_template_event'
            '_registration', False).unlink()
        with self.assertRaises(exceptions.Warning):
            self.event._send_email_to_registrations('email body')

    def test_button_validate_holiday(self):
        contract = self.contract_model.create({
            'name': u'Contract {}'.format(self.partner.name),
            'employee_id': self.ref('hr.employee_fp'),
            'partner': self.partner.id,
            'type_id': self.ref('hr_contract.hr_contract_type_emp'),
            'wage': 500,
            'date_start': '2025-01-01'})
        workable_wiz = self.wiz_workable_model.with_context(
            active_id=contract.id).create({})
        workable_wiz.button_calculate_workables_and_festives()
        holiday_vals = {
            'name': 'Rockbotic holiday',
            'holiday_status_id': self.ref('hr_holidays.holiday_status_sl'),
            'employee_id': self.ref('hr.employee_fp'),
            'date_from': '2025-06-01 08:00:00',
            'date_to': '2025-06-15 18:00:00'}
        holiday = self.holiday_model.create(holiday_vals)
        holiday.button_validate_holiday()
        subtype_id = self.ref(
            'hr_holidays.mt_holidays_confirmed')
        cond = [('model', '=', 'hr.holidays'),
                ('res_id', '=', holiday.id),
                ('subtype_id', '=', subtype_id)]
        message = self.message_model.search(cond, limit=1)
        self.assertEquals(len(message), 1,
                          'Message with holidays not found')
        self.assertIn('Date start:', message.body,
                      'Date start not found in message body')

    def test_employee_certificate(self):
        employee = self.env.ref('hr.employee_fp')
        employee.identification_id = '123456789'
        employee._compute_certificate_link()
        self.assertIn('123456789', employee.certificate_link,
                      'Bad employee certificate link')

    def test_send_email_with_evaluations(self):
        registration_vals = {'event_id': self.event.id,
                             'partner_id': self.partner.id}
        registration = self.env['event.registration'].create(
            registration_vals)
        wiz = self.email_model.create({})
        wiz.default_get(['body'])
        wiz.with_context(active_ids=registration.ids).button_send_email()
        self.assertEqual(
            registration.submitted_evaluation, 'no',
            'Bad send evaluation 1')
        self.attachment_model.create({
            'name': 'attachment 1',
            'res_model': 'event.registration',
            'res_id': registration.id})
        attachment2 = self.attachment_model.create({
            'name': 'attachment 2',
            'res_model': 'event.registration',
            'res_id': registration.id})
        wiz.with_context(active_ids=registration.ids).button_send_email()
        self.assertEqual(
            registration.submitted_evaluation, 'no',
            'Bad send evaluation 2')
        attachment2.unlink()
        try:
            parent = registration.partner_id.parent_id
            registration.partner_id.parent_id = False
            wiz.with_context(active_ids=registration.ids).button_send_email()
            self.assertEqual(
                registration.submitted_evaluation, 'no',
                'Bad send evaluation 3')
            registration.partner_id.parent_id = parent
        except:
            pass
        registration.partner_id.parent_id.email = ''
        wiz.with_context(active_ids=registration.ids).button_send_email()
        self.assertEqual(
            registration.submitted_evaluation, 'no',
            'Bad send evaluation 4')
        registration.partner_id.parent_id.email = 'parent@email.com'
        wiz.with_context(active_ids=registration.ids).button_send_email()
        self.assertEqual(
            registration.submitted_evaluation, 'yes',
            'Bad send evaluation 5')
        wiz2 = self.email2_model.create({})
        wiz2.default_get(['body'])
        wiz2.with_context(active_ids=self.event.ids).button_send_email()
        self.assertEqual(
            registration.submitted_evaluation, 'yes',
            'Bad send evaluation 6')
        self.env.ref(
            'rockbotic_custom.email_template_event_registration_evaluation',
            False).unlink()
        with self.assertRaises(exceptions.Warning):
            registration._send_email_to_registrations_with_evaluation('body')
        with self.assertRaises(exceptions.Warning):
            wiz.default_get(['body'])
        with self.assertRaises(exceptions.Warning):
            wiz2.default_get(['body'])
