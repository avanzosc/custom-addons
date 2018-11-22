# -*- coding: utf-8 -*-
# (c) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _
from openerp.tools import float_compare


class WizEventSubstitution(models.TransientModel):
    _inherit = 'wiz.event.substitution'

    @api.multi
    def button_substitution_employee(self):

        if (self.holiday and self.holiday.holiday_status_id and not
            self.holiday.holiday_status_id.limit and
                self.holiday.employee_id):
            if (self.holiday.holiday_type == 'employee' or
                    self.holiday.type == 'remove'):
                employee_id = self.holiday.employee_id.id
                leave_days = self.holiday.holiday_status_id.get_days(
                    employee_id)[self.holiday.holiday_status_id.id]
                if ((float_compare(leave_days['remaining_leaves'], 0,
                                   precision_digits=2) == 0) or
                    (float_compare(leave_days['virtual_remaining_leaves'], 0,
                                   precision_digits=2) == 0)):
                    raise exceptions.Warning(
                        _('The number of remaining leaves is not sufficient '
                          'for this leave type.\nPlease verify also the leaves'
                          ' waiting for validation.'))
        return super(WizEventSubstitution, self).button_substitution_employee()
