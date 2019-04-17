# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.addons.event_track_assistant._common import _convert_to_utc_date
from openerp.addons.event_track_assistant._common import _convert_to_local_date


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

    @api.multi
    def _compute_count_lines(self):
        for sale in self:
            sale.count_lines = len(sale.service_order_line)

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
    count_lines = fields.Integer(
        string='Sale lines', compute='_compute_count_lines')
    sale_print_line_ids = fields.One2many(
        comodel_name='sale.print.line', inverse_name='order_id',
        string='Lines to print')
    working_hours = fields.Many2one(
        comodel_name='resource.calendar', string='Working Schedule')

    @api.multi
    def action_button_confirm(self):
        event_model = self.env['event.event']
        result = super(SaleOrder, self.with_context(
            without_sale_name=True)).action_button_confirm()
        for sale in self.filtered(lambda x: x.project_id):
            cond = [('sale_order', '=', sale.id)]
            event = event_model.search(cond, limit=1)
            if event:
                event.write({'name': u"{}: {}".format(
                    sale.name, sale.partner_id.name)})
                event._merge_event_tracks()
        return result

    def _prepare_session_data_from_sale_line(
            self, event, num_session, line, date):
        vals = super(SaleOrder, self)._prepare_session_data_from_sale_line(
            event, num_session, line, date)
        vals['name'] = (_('Session %s for %s') % (str(num_session),
                                                  line.session_description))
        new_date = False
        if line.order_id.project_id:
            new_date = _convert_to_utc_date(
                date, time=line.order_id.project_id.start_time,
                tz=self.env.user.tz)
            duration = (line.order_id.project_id.end_time -
                        line.order_id.project_id.start_time)
            if line.order_id.project_id.working_hours:
                from_date = _convert_to_local_date(date, self.env.user.tz)
                day = str(from_date.date().weekday())
                lines = line.order_id.project_id.working_hours.attendance_ids
                for line2 in lines:
                    if line2.dayofweek == day:
                        new_date = _convert_to_utc_date(
                            date, time=line2.hour_from, tz=self.env.user.tz)
                        duration = line2.hour_to - line2.hour_from
        if line.start_hour or line.end_hour:
            new_date = _convert_to_utc_date(date, time=line.start_hour,
                                            tz=self.env.user.tz)
            duration = line.end_hour - line.start_hour
        if new_date:
            vals.update({'date': new_date,
                         'duration': duration})
        return vals

    @api.multi
    def button_create_sale_contract(self):
        type_hour = self.env.ref(
            'sale_order_create_event_hour.type_hour_working', False)
        for sale in self.filtered(lambda x: x.working_hours):
            year = fields.Date.from_string(
                fields.Date.context_today(self)).year
            name = u"{} {}".format(sale.partner_id.name, year)
            vals = {'name': name,
                    'type': 'contract',
                    'sale': sale.id,
                    'working_hours': sale.working_hours.id,
                    'use_timesheets': True,
                    'use_task': True,
                    'partner_id': sale.partner_id.id,
                    'type_hour': type_hour.id,
                    'recurring_invoices': True,
                    'recurring_interval': 1,
                    'recurring_rule_type': 'monthly',
                    'recurring_last_day': True}
            lines = sale.mapped('service_order_line').filtered(
                lambda l: l.start_date)
            if lines:
                l = min(lines, key=lambda x: x.start_date)
                vals['date_start'] = l.start_date
            lines = sale.mapped('service_order_line').filtered(
                lambda l: l.end_date)
            if lines:
                l = max(lines, key=lambda x: x.end_date)
                vals['date'] = l.end_date
            lines = sale.mapped('service_order_line').filtered(
                lambda l: l.start_hour)
            if lines:
                l = min(lines, key=lambda x: x.start_hour)
                vals['start_time'] = l.start_hour
            lines = sale.mapped('service_order_line').filtered(
                lambda l: l.end_hour)
            if lines:
                l = max(lines, key=lambda x: x.end_hour)
                vals['end_time'] = l.end_hour
            account = self.env['account.analytic.account'].create(vals)
            sale.project_id = account.id


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
    session_description = fields.Char(string='Session description')
    price_unit = fields.Float(readonly=False)
    product_uom_qty = fields.Float(readonly=False)
    sale_line_historical_ids = fields.One2many(
        comodel_name='sale.order.line.historical',
        inverse_name='sale_line_id', string='Sale lines historical')

    @api.multi
    def write(self, values):
        historical_obj = self.env['sale.order.line.historical']
        check_values = [
            ('price_unit', _('Price unit')),
            ('product_uom_qty', _('Quantity')),
            ('session_description', _('Session description')),
            ('january', _('January')), ('february', _('February')),
            ('march', _('March')), ('april', _('April')),
            ('may', _('May')), ('june', _('June')), ('july', _('July')),
            ('august', _('August')), ('september', _('September')),
            ('october', _('October')), ('november', _('November')),
            ('december', _('December')), ('week1', _('Week 1')),
            ('week2', _('Week 2')), ('week3', _('Week 3')),
            ('week4', _('Week 4')), ('week5', _('Week 5')),
            ('week6', _('Week 6')), ('monday', _('Monday')),
            ('tuesday', _('Tuesday')), ('wednesday', _('Wednesday')),
            ('thursday', _('Thursday')), ('friday', _('Friday')),
            ('saturday', _('Saturday')), ('sunday', _('Sunday'))]
        for value, value_name in check_values:
            if value in values:
                for l in self:
                    vals = {'sale_line_id': l.id,
                            'date': fields.Datetime.now(),
                            'user_id': self.env.uid,
                            'name':  u"{}: {}".format(
                                value_name, l.read([value])[0].get(value))}
                    historical_obj.create(vals)
        return super(SaleOrderLine, self).write(values)


class SaleOrderLineHistorical(models.Model):
    _name = 'sale.order.line.historical'
    _description = "Sale order line historical"
    _order = "date"

    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line', string="Sale order line")
    date = fields.Datetime(strin="Date")
    user_id = fields.Many2one(comodel_name='res.users', string="User")
    name = fields.Char(string="Description")


class SalePrintLine(models.Model):
    _name = 'sale.print.line'
    _description = "Sale order lines to print"

    order_id = fields.Many2one(
        comodel_name='sale.order', string="Sale order")
    product_id = fields.Many2one(
        comodel_name='product.product', domain="[('sale_ok', '=', True)]",
        string="Product")
    name = fields.Char(string='Description', required=True)
    product_uom_qty = fields.Float(
        string='Quantity', digits=dp.get_precision('Product UoS'),
        required=True)
    price_unit = fields.Float(
        string="Unit Price", digits=dp.get_precision('Product price'),
        required=True, default=0.0)
    tax_id = fields.Many2many(
        comodel_name="account.tax", relation="rel_sale_print_line_tax",
        column1="sale_print_line_id", column2="tax_id",
        string="Taxes")
    discount = fields.Float(
        string="Discount (%)",  digits=dp.get_precision('Discount'),
        default=0.0)
    price_subtotal = fields.Float(
        string="Subtotal",  digits=dp.get_precision('Account'),
        required=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            self.name = self.product_id.name
