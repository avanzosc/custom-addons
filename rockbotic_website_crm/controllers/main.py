# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import unslug


class StudentSignUp(http.Controller):

    def generate_google_map_url(self, street, city, city_zip, country_name):
        url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&"\
            "sensor=false&zoom=8&size=298x298" % werkzeug.url_quote_plus(
                '%s, %s %s, %s' % (street, city, city_zip, country_name)
            )
        return url

    def signup_values(self, group_id=None, event_id=None, data=None):
        cr, context, registry = request.cr, request.context, request.registry
        orm_partner = registry.get('res.partner')
        orm_event = registry.get('event.event')

        partner_ids = orm_partner.search(
            cr, SUPERUSER_ID, [('is_group', '=', True),
                               ('prospect', '=', False),
                               ('customer', '=', True),
                               ('payer', '=', 'student')],
            order='name', context=context)
        partner_ids = [group_id] if group_id in partner_ids else partner_ids
        groups = orm_partner.browse(cr, SUPERUSER_ID, partner_ids, context)
        event_ids = orm_event.search(
            cr, SUPERUSER_ID, [('state', 'not in', ('done', 'cancel')),
                               ('address_id', 'in', partner_ids)],
            order='name', context=context)
        event_ids = [event_id] if event_id in event_ids else event_ids
        events = orm_event.browse(cr, SUPERUSER_ID, event_ids, context)
        show_school_message = (
            groups.event_web_warning if len(groups) == 1 else False)
        values = {
            'groups': groups,
            'events': events,
            'show_school_message': show_school_message,
        }
        return values

    @http.route(['/page/student_signup', '/page/student_signup/<group_id>',
                 '/page/student_signup/<group_id>/'
                 '<model("event.event"):event>'],
                type='http', auth='public', website=True)
    def contact(self, group_id=None, event=None, **kwargs):
        if group_id:
            _, group_id = unslug(group_id)
        values = self.signup_values(
            group_id=group_id, event_id=event and event.id)
        for field in ['partner_name', 'phone', 'contact_name', 'email_from',
                      'name']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(values={}, kwargs=kwargs.items())
        return request.website.render(
            "rockbotic_website_crm.student_signup", values)

    def create_lead(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context
        school = request.registry['res.partner'].browse(
            cr, SUPERUSER_ID, int(values.get('school_id')), context=context)
        values.update({
            'user_id': school.user_id.id,
        })
        return request.registry['crm.lead'].create(
            cr, SUPERUSER_ID, values,
            context=dict(context, mail_create_nosubscribe=True,
                         default_type='enroll'))

    def preRenderThanks(self, values, kwargs):
        """ Allow to be overrided """
        company = request.website.company_id
        return {
            'google_map_url': self.generate_google_map_url(
                company.street, company.city, company.zip,
                company.country_id and company.country_id.name_get()[0][1] or
                ''),
            '_values': values,
            '_kwargs': kwargs,
        }

    def get_contactus_response(self, values, kwargs):
        values = self.preRenderThanks(values, kwargs)
        return request.website.render(
            kwargs.get("view_callback",
                       "rockbotic_website_crm.student_signup_thanks"), values)

    @http.route(['/crm/student_signup'],
                type='http', auth="public", website=True)
    def contactus(self, **kwargs):
        def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

        _TECHNICAL = ['show_info', 'view_from', 'view_callback']
        # Only use for behavior, don't stock it
        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid',
                      'write_date', 'user_id', 'active']
        # Allow in description
        _REQUIRED = ['name', 'student_name', 'student_surname1',
                     'parent_name', 'parent_surname1', 'birth_date',
                     'journal_permission', 'blog_permission',
                     'media_permission']
        # Could be improved including required from model

        # List of file to add to ir_attachment once we have the ID
        post_file = []
        post_description = []  # Info to add after the message
        values = {}

        model_data = request.registry['ir.model.data']
        values['medium_id'] = model_data.xmlid_to_res_id(
            request.cr, SUPERUSER_ID,
            'rockbotic_website_crm.crm_medium_student_signup')
        values['section_id'] = model_data.xmlid_to_res_id(
            request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, 'filename'):
                post_file.append(field_value)
            elif field_name in request.registry['crm.lead']._fields and\
                    field_name not in _BLACKLIST:
                values[field_name] = field_value
            elif field_name not in _TECHNICAL:
                # allow to add some free fields or blacklisted field like ID
                post_description.append("%s: %s" % (field_name, field_value))

        if values.get('student_surname2', '') != '':
            student_name = u'{} {}, {}'.format(
                values.get('student_surname1').capitalize(),
                values.get('student_surname2').capitalize(),
                values.get('student_name').capitalize())
        else:
            student_name = u'{}, {}'.format(
                values.get('student_surname1').capitalize(),
                values.get('student_name').capitalize())

        if values.get('parent_surname2', '') != '':
            parent_name = u'{} {}, {}'.format(
                values.get('parent_surname1').capitalize(),
                values.get('parent_surname2').capitalize(),
                values.get('parent_name').capitalize())
        else:
            parent_name = u'{}, {}'.format(
                values.get('parent_surname1').capitalize(),
                values.get('parent_name').capitalize())

        values.update({
            'contact_name': student_name,
            'partner_name': parent_name,
            'school_id': int(values.get('school_id') or 0),
            'event_id': int(values.get('event_id') or 0),
            'rockbotic_before': (
                True if values.get('rockbotic_before') == 'on' else False),
            'opt_out': (
                True if values.get('opt_out') == 'on' else False),
            'no_confirm_mail': (
                True if values.get('no_confirm_mail') == 'on' else False),
            'accept_whatsapp': (
                True if values.get('accept_whatsapp') else False),
            'accept_center_information': (
                True if values.get('accept_center_information') else False),
        })

        if "name" not in kwargs and values.get("contact_name"):
            # if kwarg.name is empty, it's an error, we cannot copy
            # the contact_name
            values["name"] = values.get("contact_name")

        # fields validation : Check that required field from
        # model crm_lead exists
        error = set(field for field in _REQUIRED if not values.get(field))

        if values.get('vat'):
            vat = (
                u'ES{}'.format(values.get('vat'))
                if len(values.get('vat')) == 9 else values.get('vat'))
            orm_partner = request.registry['res.partner']
            vat_country, vat_number = orm_partner._split_vat(vat)
            if not orm_partner.simple_vat_check(
                    request.cr, SUPERUSER_ID, vat_country, vat_number):
                error.add('vat')
                # The VAT number does not seem to be valid

        iban = values.get('account_number')
        orm_bank = request.registry['res.partner.bank']
        if not orm_bank.is_iban_valid(request.cr, SUPERUSER_ID, iban):
            error.add('account_number')
            # The IBAN does not seem to be correct.

        if error:
            signup_values = self.signup_values(
                group_id=values.get('school_id'),
                event_id=values.get('event_id'))
            values = dict(
                signup_values, values=values, error=error,
                kwargs=kwargs.items())
            return request.website.render(kwargs.get(
                "view_from", "rockbotic_website_crm.student_signup"), values)

        # description is required, so it is always already initialized
        if post_description:
            values['description'] += dict_to_str(_("Custom Fields: "),
                                                 post_description)

        if kwargs.get("show_info"):
            post_description = []
            environ = request.httprequest.headers.environ
            post_description.append("%s: %s" %
                                    ("IP", environ.get("REMOTE_ADDR")))
            post_description.append("%s: %s" %
                                    ("USER_AGENT",
                                     environ.get("HTTP_USER_AGENT")))
            post_description.append("%s: %s" %
                                    ("ACCEPT_LANGUAGE",
                                     environ.get("HTTP_ACCEPT_LANGUAGE")))
            post_description.append("%s: %s" %
                                    ("REFERER", environ.get("HTTP_REFERER")))
            values['description'] += dict_to_str(_("Environ Fields: "),
                                                 post_description)

        lead_id = self.create_lead(request, dict(values, user_id=False),
                                   kwargs)
        values.update(lead_id=lead_id)
        if lead_id:
            for field_value in post_file:
                attachment_value = {
                    'name': field_value.filename,
                    'res_name': field_value.filename,
                    'res_model': 'crm.lead',
                    'res_id': lead_id,
                    'datas': base64.encodestring(field_value.read()),
                    'datas_fname': field_value.filename,
                }
                request.registry['ir.attachment'].create(
                    request.cr, SUPERUSER_ID, attachment_value,
                    context=request.context)

        return self.get_contactus_response(values, kwargs)
