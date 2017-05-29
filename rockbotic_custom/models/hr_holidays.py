# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.multi
    def button_validate_holiday(self):
        message_obj = self.env['mail.message']
        subtype = self.env.ref(
            'hr_holidays.mt_holidays_confirmed', False)
        super(HrHolidays, self).button_validate_holiday()
        if subtype:
            for holiday in self:
                cond = [('model', '=', 'hr.holidays'),
                        ('res_id', '=', holiday.id),
                        ('subtype_id', '=', subtype.id)]
                message = message_obj.search(cond, limit=1)
                if message:
                    message.body = _(
                        u'<span><span style="font-weight: bold;">Date start:'
                        u'</span> {} <span style="font-weight: bold;">Date end'
                        u':</span> {} <span style="font-weight: bold;">days:'
                        u'</span> {}<br></span>{}'.format(
                            fields.Datetime.from_string(
                                holiday.date_from).date(),
                            fields.Datetime.from_string(
                                holiday.date_to).date(),
                            holiday.number_of_days_temp, message.body))
