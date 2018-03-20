# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions
from openerp import fields


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
        self.account_model = self.env['account.analytic.account']
        self.sale_model = self.env['sale.order']
        self.translation_obj = self.env['ir.translation']
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
        self.contract_model.create({
            'name': u'Contract {}'.format(self.partner.name),
            'employee_id': self.ref('hr.employee_fp'),
            'partner': self.partner.id,
            'type_id': self.ref('hr_contract.hr_contract_type_emp'),
            'wage': 500,
            'date_start': '2025-01-01'})
        holiday_vals = {
            'name': 'Rockbotic holiday',
            'holiday_status_id': self.ref('hr_holidays.holiday_status_sl'),
            'employee_id': self.ref('hr.employee_fp'),
            'date_from': '2025-06-01 08:00:00',
            'date_to': '2025-06-15 18:00:00'}
        holiday = self.holiday_model.create(holiday_vals)
        holiday.button_validate_holiday()
        subtype_id = self.ref('hr_holidays.mt_holidays_confirmed')
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
        except Exception:
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

    def test_rockbotic_sale_order(self):
        account_vals = {'name': 'Analytic account for Rockbotic test',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28',
                        'use_tasks': True}
        self.account = self.account_model.create(account_vals)
        sale_vals = {
            'name': 'sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'project_id': self.account.id,
            'project_by_task': 'no',
        }
        self.service_product = self.browse_ref(
            'product.product_product_consultant')
        sale_line_vals = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uom_qty': 7,
            'product_uom': self.service_product.uom_id.id,
            'price_unit': self.service_product.list_price,
            'performance': self.service_product.performance,
            'january': True,
            'february': True,
            'week4': True,
            'week5': True,
            'tuesday': True,
            'thursday': True,
            'start_date': '2025-01-15',
            'start_hour': 8.00,
            'end_date': '2025-02-28',
            'end_hour': 09.00}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.sale_order.order_line[0].button_group_description()
        res = self.sale_order._prepare_recurring_invoice_lines(
            self.sale_order.order_line[0])
        self.assertIn(
            self.sale_order.order_line[0].group_description, res.get('name'),
            'Bad name for recurring invoice line')
        new_order = self.sale_order.copy()
        self.assertIn(
            new_order.name, new_order.order_line[0].group_description,
            'Bad group description for new sale order line')

    def test_rockbotic_group_description(self):
        self.event.sale_order_line.write(
            {'group_description': 'changed group description'})
        vals = {'lang': 'en_US',
                'name': 'event.event,name',
                'res_id': self.event.id,
                'type': 'model',
                'src': 'test rockbotic_custom',
                'value': 'changed group description'}
        self.translation_obj.create(vals)
        self.event.group_description = 'changed group description'
        self.event.onchange_group_description()
        self.assertEqual(
            self.event.group_description, self.event.name,
            'Event name not equal group description')
        cond = [('lang', '=', 'es_ES'),
                ('name', '=', 'event.event,name'),
                ('res_id', '=', self.event.id),
                ('type', '=', 'model')]
        translation = self.translation_obj.search(cond, limit=1)
        if translation:
            self.assertEqual(
                len(translation), 1,
                'Translation not found for event name')
            self.assertEqual(
                translation.src, translation.value,
                'Bad translation for event name')

    def test_rockbotic_account_name(self):
        account_vals = {'name': 'Parent Analytic account for Rockbotic test',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28',
                        'use_tasks': True}
        parent_account = self.account_model.create(account_vals)
        account_vals = {'name': 'Child Analytic account for Rockbotic test',
                        'date_start': '2025-01-15',
                        'date': '2025-02-28',
                        'use_tasks': True,
                        'parent_id': parent_account.id}
        child_account = self.account_model.create(account_vals)
        res = child_account.name_get()[0][1]
        self.assertIn(parent_account.name, res,
                      'Parent name not found in children name')
        res = child_account.with_context(only_name=True).name_get()[0][1]
        self.assertNotIn(parent_account.name, res,
                         'Parent name found in children name')

    def test_prepare_wizard_registration_open_vals(self):
        today = fields.Date.from_string(fields.Date.today())
        new_date = '{}-{}-01'.format(today.year, today.month)
        self.event_date_begin = '2016-12-12 15:00:00'
        registration_vals = {'event_id': self.event.id,
                             'partner_id': self.partner.id,
                             'date_start': '2016-12-12 15:00:00'}
        registration = self.env['event.registration'].create(
            registration_vals)
        vals = registration._prepare_wizard_registration_open_vals()
        self.assertEqual(
            vals.get('from_date', False), new_date,
            'Bad from_date in registration')
