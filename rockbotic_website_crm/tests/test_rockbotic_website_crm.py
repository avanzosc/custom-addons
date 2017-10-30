# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.rockbotic_custom.tests.test_rockbotic_custom import\
    TestRockboticCustom
from openerp import exceptions, fields
from openerp.addons.base_iban.base_iban import _format_iban, _pretty_iban
from openerp.addons.website.models.website import slug


class TestRockboticWebsiteCrm(TestRockboticCustom):

    def setUp(self):
        super(TestRockboticWebsiteCrm, self).setUp()
        self.partner_model = self.env['res.partner']
        self.mail_model = self.env['mail.mail']
        self.enroll_model = self.env['crm.lead']
        self.search_action = self.browse_ref(
            'rockbotic_website_crm.res_partner_enroll_search_action')
        self.enroll_action = self.browse_ref(
            'rockbotic_website_crm.action_crm_lead2opportunity_partner')
        self.parent.mapped('bank_ids.mandate_ids').filtered(
            lambda m: m.state in ('draft', 'valid')).cancel()
        self.iban_acc_number = 'ES2715688807689087558775'
        account_type = self.env.ref('base_iban.bank_iban')
        self.parent.write({
            'bank_ids': [(0, 0, {
                'state': account_type.code,
                'acc_number': self.iban_acc_number,
                'mandate_ids': [(0, 0, {
                    'format': 'sepa',
                    'type': 'recurrent',
                    'recurrent_sequence_type': 'recurring',
                    'signature_date': fields.Date.today(),
                })],
            })],
        })
        self.parent.mapped('bank_ids.mandate_ids').filtered(
            lambda m: m.state == 'draft').validate()
        self.school = self.partner_model.create({
            'name': 'School',
            'is_group': True,
            'payer': 'student',
        })
        self.event.write({
            'address_id': self.school.id,
        })
        self.enrollment = self.enroll_model.create({
            'name': 'TEST',
            'contact_name': self.partner.name,
            'partner_name': self.parent.name,
            'vat': self.parent.vat,
            'zip': self.parent.zip,
            'rockbotic_before': False,
            'journal_permission': 'no',
            'blog_permission': 'no',
            'media_permission': 'no',
            'birth_date': fields.Date.today(),
            'account_number': self.iban_acc_number,
            'type': 'enroll',
            'school_id': self.school.id,
            'event_id': self.event.id,
            'medium_id': self.ref(
                'rockbotic_website_crm.crm_medium_student_signup'),
        })
        self.search_wiz = self.env['res.partner.enroll.search']
        self.enroll_wiz = self.env['crm.lead2opportunity.partner']

    def test_enrollment_new(self):
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.assertFalse(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])
        search_wiz = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        self.assertFalse(search_wiz.rockbotic_before)
        enroll_dict = self.enroll_action.read()[0] if self.enroll_action else\
            {}
        button_dict = search_wiz.action_apply()
        self.assertTrue(self.enrollment.partner_id)
        self.assertNotEquals(self.enrollment.partner_id, self.partner)
        self.assertTrue(self.enrollment.parent_id)
        self.assertNotEquals(self.enrollment.parent_id, self.parent)
        self.assertEquals(self.enrollment.partner_id.name,
                          self.enrollment.contact_name)
        self.assertEquals(self.enrollment.partner_id.parent_id.name,
                          self.enrollment.partner_name)
        self.assertEquals(self.enrollment.journal_permission == 'yes',
                          self.enrollment.partner_id.magazine)
        self.assertEquals(self.enrollment.blog_permission == 'yes',
                          self.enrollment.partner_id.web_blog)
        self.assertEquals(self.enrollment.media_permission == 'yes',
                          self.enrollment.partner_id.social_networks)
        self.assertEquals(self.enrollment.course,
                          self.enrollment.partner_id.student_class)
        self.assertEquals(self.enrollment.birth_date,
                          self.enrollment.partner_id.birthdate_date)
        self.assertEquals(button_dict['res_model'], enroll_dict['res_model'])
        self.assertEquals(button_dict['name'], enroll_dict['name'])
        enroll_wiz = self.enroll_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        self.assertTrue(enroll_wiz.partner_id)
        self.assertTrue(enroll_wiz.parent_id)
        enroll_wiz.action_apply()
        self.assertTrue(self.enrollment.event_registration_id)

    def test_enrollment_new2(self):
        enrollment = self.enroll_model.create({
            'name': 'TEST',
            'contact_name': 'children',
            'partner_name': 'father',
            'vat': '15252683A',
            'zip': 20720,
            'rockbotic_before': False,
            'journal_permission': 'no',
            'blog_permission': 'no',
            'media_permission': 'no',
            'birth_date': fields.Date.today(),
            'account_number': 'ES2715688807689087558775',
            'type': 'enroll',
            'school_id': self.school.id,
            'event_id': self.event.id,
            'medium_id': self.ref(
                'rockbotic_website_crm.crm_medium_student_signup'),
            'no_confirm_mail': False,
            'email_from': 'test@rockbotic.com'
        })
        cond = [('name', '=', 'test@rockbotic.com'),
                ('display_name', '=', 'test@rockbotic.com'),
                ('email', '=', 'test@rockbotic.com'),
                ('type', '=', 'contact')]
        partner = self.partner_model.search(cond, limit=1)
        self.assertEquals(len(partner), 1,
                          'Automatic created partner not found')
        self.assertEquals(partner.delete_after_sending_email, True,
                          'Partner not marked to delete')
        cond = [('recipient_ids', 'in', [partner.id])]
        mail = self.mail_model.search(cond, limit=1)
        self.assertEquals(len(mail), 1,
                          'First email not found')
        enrollment.school_id.user_id = 1
        enrollment._onchange_school_id()
        self.assertEquals(enrollment.user_id, enrollment.school_id.user_id,
                          'Bad school user')
        self.browse_ref(
            'rockbotic_website_crm.email_to_new_enrollment').unlink()
        with self.assertRaises(exceptions.Warning):
            enrollment = self.enroll_model.create({
                'name': 'TEST 2',
                'contact_name': 'children 2',
                'partner_name': 'father 2',
                'vat': '15252683A',
                'zip': 20720,
                'rockbotic_before': False,
                'journal_permission': 'no',
                'blog_permission': 'no',
                'media_permission': 'no',
                'birth_date': fields.Date.today(),
                'account_number': 'ES2715688807689087558775',
                'type': 'enroll',
                'school_id': self.school.id,
                'event_id': self.event.id,
                'medium_id': self.ref(
                    'rockbotic_website_crm.crm_medium_student_signup'),
                'no_confirm_mail': False,
                'email_from': 'test3@rockbotic.com'
            })
        self.assertFalse(self.enrollment.event_registration_id)
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.assertFalse(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])
        search_wiz = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({
                'parent_id': self.parent.id
            })
        search_wiz.action_apply()
        self.assertNotEquals(self.enrollment.partner_id, self.partner)
        self.assertEquals(self.enrollment.parent_id, self.parent)
        enroll_wiz = self.enroll_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        self.browse_ref(
            'rockbotic_website_crm.email_sepa_to_new_registration_from_'
            'enrollment').unlink()
        with self.assertRaises(exceptions.Warning):
            enroll_wiz.action_apply()
        self.browse_ref(
            'rockbotic_website_crm.email_to_new_registration_from_'
            'enrollment').unlink()
        with self.assertRaises(exceptions.Warning):
            enroll_wiz.action_apply()

    def test_enrollment_parent_exist(self):
        self.assertFalse(self.enrollment.event_registration_id)
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.assertFalse(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])
        search_wiz = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({
                'parent_id': self.parent.id
            })
        search_wiz.action_apply()
        self.assertNotEquals(self.enrollment.partner_id, self.partner)
        self.assertEquals(self.enrollment.parent_id, self.parent)
        enroll_wiz = self.enroll_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        enroll_wiz.action_apply()
        self.assertTrue(self.enrollment.event_registration_id)
        self.assertEquals(self.enrollment.event_registration_id.partner_id,
                          self.enrollment.partner_id)
        self.assertEquals(self.enrollment.event_registration_id.event_id,
                          self.enrollment.event_id)
        self.assertEquals(self.enrollment.partner_id.parent_id, self.parent)

    def test_enrollment_rbk(self):
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.enrollment.rockbotic_before = True
        self.assertTrue(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])
        search_wiz_dict = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).default_get([])
        self.assertTrue(search_wiz_dict['rockbotic_before'])
        with self.assertRaises(exceptions.ValidationError):
            self.search_wiz.create(search_wiz_dict)
        self.assertTrue(search_wiz_dict['item_ids'])
        search_wiz_dict['item_ids'][0][2].update({'checked': True})
        search_wiz = self.search_wiz.create(search_wiz_dict)
        search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name
        ).action_apply_same_parent()
        self.assertEquals(self.enrollment.partner_id, self.partner)
        self.assertEquals(self.enrollment.parent_id, self.parent)
        enroll_wiz = self.enroll_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        enroll_wiz.action_apply()
        self.assertTrue(self.enrollment.event_registration_id)

    def test_enrollment_rbk_change_parent(self):
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.enrollment.rockbotic_before = True
        self.assertTrue(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])
        search_wiz_dict = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).default_get([])
        search_wiz_dict['item_ids'][0][2].update({'checked': True})
        search_wiz = self.search_wiz.create(search_wiz_dict)
        search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).action_apply()
        self.assertEquals(self.enrollment.partner_id, self.partner)
        self.assertNotEquals(self.enrollment.parent_id, self.parent)

    def test_enrollment_rbk_change_account(self):
        new_iban = _pretty_iban(_format_iban('ES3759142809123095976574'))
        self.enrollment.write({
            'rockbotic_before': True,
            'account_number': new_iban,
        })
        old_mandate = self.parent.mapped(
            'bank_ids.mandate_ids').filtered(lambda m: m.state == 'valid')
        self.assertEquals(len(old_mandate), 1)
        self.assertTrue(self.parent.bank_ids.filtered(
            lambda b: b.acc_number == _pretty_iban(_format_iban(
                self.iban_acc_number))))
        self.assertFalse(self.parent.bank_ids.filtered(
            lambda b: b.acc_number == new_iban))
        search_wiz_dict = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).default_get([])
        search_wiz_dict['item_ids'][0][2].update({'checked': True})
        search_wiz = self.search_wiz.create(search_wiz_dict)
        search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name
        ).action_apply_same_parent()
        new_bank = self.parent.bank_ids.filtered(
            lambda b: b.acc_number == new_iban)
        self.assertTrue(new_bank)
        self.assertEquals(len(new_bank.mandate_ids), 1)
        self.assertEquals(old_mandate[:1].state, 'cancel')

    def test_enrollment_with_partners(self):
        self.enrollment.write({
            'partner_id': self.partner.id,
            'parent_id': self.partner.parent_id.id,
        })
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.enroll_action.read()[0] if self.enroll_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        self.assertEquals(button_dict['name'], action_dict['name'])

    def test_enrollment_list(self):
        self.enrollment.vat = 'ES84541728F' if not self.enrollment.vat else \
            self.enrollment.vat
        self.assertFalse(self.enrollment.rockbotic_before)
        self.assertTrue(self.enrollment.vat)
        enroll_same_parent = self.enrollment.copy()
        enroll_same_parent.write({'contact_name': 'Sibling'})
        self.assertNotEquals(self.enrollment.contact_name,
                             enroll_same_parent.contact_name)
        self.assertEquals(self.enrollment.vat, enroll_same_parent.vat)
        self.assertFalse(self.enrollment.rockbotic_before)
        new_enroll = self.enrollment.copy()
        new_enroll.write({'vat': 'ES28614426B'})
        self.assertNotEquals(self.enrollment.vat, new_enroll.vat)
        self.assertFalse(self.enrollment.rockbotic_before)
        no_enroll = self.enrollment.copy()
        no_enroll.write({'rockbotic_before': True})
        enrolls = self.enrollment | enroll_same_parent | new_enroll | no_enroll
        enrolls.create_registrations()
        self.assertTrue(self.enrollment.event_registration_id)
        self.assertTrue(enroll_same_parent.event_registration_id)
        self.assertTrue(new_enroll.event_registration_id)
        self.assertFalse(no_enroll.event_registration_id)
        self.assertEquals(self.enrollment.parent_id,
                          enroll_same_parent.parent_id)
        self.assertNotEquals(self.enrollment.partner_id,
                             enroll_same_parent.partner_id)
        self.assertNotEquals(self.enrollment.parent_id,
                             new_enroll.parent_id)

    def test_slug_links(self):
        self.assertFalse(self.school.signup_slug)
        self.assertTrue(self.school.is_group)
        self.assertTrue(self.school.customer)
        self.assertEquals(self.school.payer, 'student')
        self.assertTrue(self.school.prospect)
        self.school.prospect = False  # this is just to force slug creation
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url', default='http://madrid.rockbotic.com')
        self.assertFalse(self.school.prospect)
        school_slug = '{}/page/student_signup/{}'.format(
            base_url, slug(self.school))
        self.school.button_recompute_slug()
        self.assertEquals(self.school.signup_slug, school_slug)
        event_slug = '{}/{}'.format(
            self.event.address_id.signup_slug, slug(self.event))
        self.event.button_recompute_slug()
        self.assertEquals(self.event.signup_slug, event_slug)

    def test_rockbotic_custom(self):
        """ pass """

    def test_analytic_recurring(self):
        """ pass """

    def test_send_email(self):
        """ pass """

    def test_button_validate_holiday(self):
        """ pass """

    def test_employee_certificate(self):
        """ pass """

    def test_send_email_with_evaluations(self):
        """ pass """
