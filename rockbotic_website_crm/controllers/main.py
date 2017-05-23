# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _


class StudentSignUp(http.Controller):

    def generate_google_map_url(self, street, city, city_zip, country_name):
        url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&"\
            "sensor=false&zoom=8&size=298x298" % werkzeug.url_quote_plus(
                '%s, %s %s, %s' % (street, city, city_zip, country_name)
            )
        return url

    @http.route(['/page/website.student_signup', '/page/student_signup'],
                type='http', auth='public', website=True)
    def contact(self, **kwargs):
        cr, context, registry = request.cr, request.context, request.registry
        orm_partner = registry.get('res.partner')
        orm_event = registry.get('event.event')

        partner_ids = orm_partner.search(
            cr, SUPERUSER_ID, [('is_group', '=', True),
                               ('prospect', '=', False),
                               ('customer', '=', True),
                               ('payer', '=', 'student')], context=context)
        groups = orm_partner.browse(cr, SUPERUSER_ID, partner_ids, context)
        event_ids = orm_event.search(
            cr, SUPERUSER_ID, [('state', 'not in', ('done', 'cancel'))],
            context=context)
        events = orm_event.browse(cr, SUPERUSER_ID, event_ids, context)
        values = {
            'zip': '',
            'groups': groups,
            'events': events,
        }
        for field in ['partner_name', 'phone', 'contact_name', 'email_from',
                      'name']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("website.student_signup", values)

    def create_lead(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context
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
        _REQUIRED = ['name', 'partner_name', 'contact_name', 'email_from',
                     'birth_date', 'course', 'journal_permission',
                     'blog_permission', 'media_permission']
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

        if "name" not in kwargs and values.get("contact_name"):
            # if kwarg.name is empty, it's an error, we cannot copy
            # the contact_name
            values["name"] = values.get("contact_name")
        # fields validation : Check that required field from
        # model crm_lead exists
        error = set(field for field in _REQUIRED if not values.get(field))

        if error:
            values = dict(values, error=error, kwargs=kwargs.items())
            return request.website.render(kwargs.get(
                "view_from", "website.student_signup"), values)

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
