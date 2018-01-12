# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_services_amounts(self):
        for sale in self:
            cur = sale.pricelist_id.currency_id
            total = 0.00
            taxes = 0.00
            for line in sale._get_service_lines():
                total += line.monthly_amount
                for c in line.tax_id.compute_all(
                        1.00, line.monthly_amount, line.product_id,
                        line.order_id.partner_id)['taxes']:
                    taxes += c.get('amount', 0.0)
            sale.services_amount_untaxed = cur.round(total)
            sale.services_amount_tax = cur.round(taxes)
            sale.services_amount_total = (
                sale.services_amount_untaxed + sale.services_amount_tax)

    def _get_service_lines(self):
        return self.service_order_line.filtered(
            lambda x: 'semiproductivo' not in x.product_id.name_template and
            'traslados' not in x.product_id.name_template)

    amount_untaxed = fields.Float(
        string='Untaxed Amount', digits=dp.get_precision('Precision in sales'))
    amount_tax = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))
    amount_total = fields.Float(
        string='Total', digits=dp.get_precision('Precision in sales'))
    services_amount_untaxed = fields.Float(
        string='Services untaxed amount',
        digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')
    services_amount_tax = fields.Float(
        string='Services taxes', digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')
    services_amount_total = fields.Float(
        string='Services amount total',
        digits=dp.get_precision('Precision in sales'),
        compute='_compute_services_amounts')

    @api.multi
    def action_button_confirm(self):
        event_model = self.env['event.event']
        if (any(self.mapped('order_line.product_id.recurring_service')) and
                self.project_id):
            self._put_days_in_working_hours()
        result = super(SaleOrder, self.with_context(
            without_sale_name=True)).action_button_confirm()
        for sale in self.filtered(lambda x: x.project_id):
            cond = [('sale_order', '=', sale.id)]
            event = event_model.search(cond, limit=1)
            if event:
                event.write({'name': u"{}: {}".format(
                    sale.name, sale.partner_id.name)})
                event._merge_event_tracks()
                sale.project_id._recalculate_sessions_date_from_calendar()
        return result

    @api.multi
    def _put_days_in_working_hours(self):
        calendar_obj = self.env['resource.calendar']
        for sale in self:
            if not sale.project_id.working_hours:
                sale.project_id.working_hours = calendar_obj.create(
                    {'name': sale.project_id.name})
            lines = sale.order_line.filtered(
                lambda x: x.product_id.recurring_service and
                (not x.start_date or not x.end_date) and
                (x.monday or x.tuesday or x.wednesday or x.thursday or
                 x.friday or x.saturday or x.sunday))
            sale._confirm_days_in_working_hours(lines)

    def _confirm_days_in_working_hours(self, lines):
        hour_from = self.project_id.start_time
        hour_to = self.project_id.end_time
        for line in lines:
            days = self.project_id.working_hours.attendance_ids
            vals = []
            if (line.monday and not any(days.filtered(lambda x:
                                                      x.dayofweek == '0'))):
                vals.append((0, 0, {'name': _('Monday'), 'dayofweek': '0',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.tuesday and not any(days.filtered(lambda x:
                                                       x.dayofweek == '1'))):
                vals.append((0, 0, {'name': _('Tuesday'), 'dayofweek': '1',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.wednesday and not any(days.filtered(lambda x:
                                                         x.dayofweek == '2'))):
                vals.append((0, 0, {'name': _('Wednesday'), 'dayofweek': '2',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.thursday and not any(days.filtered(lambda x:
                                                        x.dayofweek == '3'))):
                vals.append((0, 0, {'name': _('Thursday'), 'dayofweek': '3',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.friday and not any(days.filtered(lambda x:
                                                      x.dayofweek == '4'))):
                vals.append((0, 0, {'name': _('Friday'), 'dayofweek': '4',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.saturday and not any(days.filtered(lambda x:
                                                        x.dayofweek == '5'))):
                vals.append((0, 0, {'name': _('Saturday'), 'dayofweek': '5',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if (line.sunday and not any(days.filtered(lambda x:
                                                      x.dayofweek == '6'))):
                vals.append((0, 0, {'name': _('Sunday'), 'dayofweek': '6',
                                    'hour_from': hour_from,
                                    'hour_to': hour_to}),)
            if vals:
                self.project_id.working_hours.write({'attendance_ids': vals})

    def _prepare_session_data_from_sale_line(
            self, event, num_session, line, date):
        vals = super(SaleOrder, self)._prepare_session_data_from_sale_line(
            event, num_session, line, date)
        vals['name'] = (_('Session %s for %s') % (str(num_session), line.name))
        return vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_id', 'product_tmpl_id')
    def _compute_product_type(self):
        super(SaleOrderLine, self)._compute_product_type()
        for line in self:
            if not line.product_type and line.product_tmpl_id:
                line.product_type = line.product_tmpl_id.type

    def _compute_service_time(self):
        for line in self:
            seconds = line.weekly_hours * 3600
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            line.service_time = "%d:%02d:%02d" % (h, m, s)

    apply_performance = fields.Boolean(default=False)
    price_unit = fields.Float(
        string='Unit Price', digits=dp.get_precision('Precision in sales'))
    price_subtotal = fields.Float(
        string='Subtotal', digits=dp.get_precision('Precision in sales'))
    periodicity = fields.Char(string='Periodicity')
    service_time = fields.Char(
        string='Service time', compute='_compute_service_time')
