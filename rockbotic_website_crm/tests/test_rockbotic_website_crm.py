# -*- coding: utf-8 -*-
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.rockbotic_custom.tests.test_rockbotic_custom import\
    TestRockboticCustom
from openerp import fields


class TestRockboticWebsiteCrm(TestRockboticCustom):

    def setUp(self):
        super(TestRockboticWebsiteCrm, self).setUp()
        enroll_model = self.env['crm.lead']
        self.search_action = self.browse_ref(
            'rockbotic_website_crm.res_partner_enroll_search_action')
        school = self.partner_model.create({
            'name': 'School',
            'is_group': True,
            'payer': 'student',
        })
        self.event.write({
            'address_id': school.id,
        })
        self.enrollment = enroll_model.create({
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
            'account_number': 'ES2715688807689087558775',
            'type': 'enroll',
            'school_id': school.id,
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
        search_wiz = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        self.assertFalse(search_wiz.rockbotic_before)
        enroll_action = self.browse_ref(
            'rockbotic_website_crm.action_crm_lead2opportunity_partner')
        enroll_dict = search_wiz.action_apply()
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
        self.assertEquals(enroll_dict['res_model'], enroll_action['res_model'])
        enroll_wiz = self.enroll_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).create({})
        self.assertTrue(enroll_wiz.partner_id)
        self.assertTrue(enroll_wiz.parent_id)
        enroll_wiz.action_apply()
        self.assertTrue(self.enrollment.event_registration_id)

    def test_enrollment_parent_exist(self):
        self.assertFalse(self.enrollment.event_registration_id)
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.assertFalse(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
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

    def test_enrollment_rbk(self):
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.enrollment.rockbotic_before = True
        self.assertTrue(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])
        search_wiz_dict = self.search_wiz.with_context(
            active_id=self.enrollment.id,
            active_ids=self.enrollment.ids,
            active_model=self.enrollment._model._name).default_get([])
        self.assertTrue(search_wiz_dict['rockbotic_before'])

    def test_enrollment_rbk_change_parent(self):
        self.assertFalse(self.enrollment.partner_id)
        self.assertFalse(self.enrollment.parent_id)
        self.enrollment.rockbotic_before = True
        self.assertTrue(self.enrollment.rockbotic_before)
        button_dict = self.enrollment.button_convert2opportunity()
        action_dict = self.search_action.read()[0] if self.search_action else\
            {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])

    def test_enrollment_with_partners(self):
        self.enrollment.write({
            'partner_id': self.partner.id,
            'parent_id': self.partner.parent_id.id,
        })
        button_dict = self.enrollment.button_convert2opportunity()
        action = self.browse_ref(
            'rockbotic_website_crm.action_crm_lead2opportunity_partner')
        action_dict = action.read()[0] if action else {}
        self.assertEquals(button_dict['res_model'], action_dict['res_model'])

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
