# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id:
            self.product_id = self.lot_id.product_id.id
        return super(MrpRepair, self).onchange_lot_id()

    @api.multi
    @api.onchange('product_id', 'lot_id')
    def onchange_product_id(self, product_id=None):
        res = super(MrpRepair, self).onchange_product_id(product_id=product_id)
        if res['value'] and 'lot_id' in res['value']:
            del res['value']['lot_id']
        return res

    def _defaul_quotation_notes(self):
        return self.env.user.company_id.sale_note

    @api.depends('partner_id', 'operations', 'fees_lines', 'operations.tax_id',
                 'operations.to_invoice', 'operations.price_unit',
                 'operations.expected_qty', 'operations.product_uom_qty',
                 'operations.product_id', 'operations.discount',
                 'operations.discount2', 'operations.discount3',
                 'operations.price_subtotal', 'fees_lines.to_invoice',
                 'fees_lines.tax_id', 'fees_lines.price_unit',
                 'fees_lines.product_uom_qty', 'fees_lines.product_id',
                 'fees_lines.discount', 'fees_lines.discount2',
                 'fees_lines.discount3', 'fees_lines.price_subtotal')
    @api.multi
    def _compute_repair_amount(self):
        for repair in self:
            untaxed = taxed = 0.0
            operation_subtotal = fee_subtotal = last_cost_total = 0.0
            real_hours_cost = real_hours_qty = 0.0
            for line in repair.operations:
                operation_subtotal = operation_subtotal + line.cost_subtotal
                last_cost_total = last_cost_total + \
                    line.last_purchase_price_valued
                if line.to_invoice:
                    untaxed += line.price_subtotal
                    qty = line.expected_qty or line.product_uom_qty
                    price = (line.price_unit *
                             (1 - (line.discount or 0.0) / 100) *
                             (1 - (line.discount2 or 0.0) / 100) *
                             (1 - (line.discount3 or 0.0) / 100))
                    tax_calculate = line.tax_id.compute_all(
                        price, qty, line.product_id, repair.partner_id)
                    taxed += sum(x['amount'] for x in tax_calculate['taxes'])
            for line in repair.fees_lines:
                fee_subtotal = fee_subtotal + line.cost_subtotal
                if line.is_from_menu:
                    # Coste horas reales creadas desde menu
                    real_hours_cost = real_hours_cost + line.cost_subtotal
                    real_hours_qty = real_hours_qty + line.product_uom_qty
                if line.to_invoice:
                    untaxed += line.price_subtotal
                    price = (line.price_unit *
                             (1 - (line.discount or 0.0) / 100) *
                             (1 - (line.discount2 or 0.0) / 100) *
                             (1 - (line.discount3 or 0.0) / 100))
                    tax_calculate = line.tax_id.compute_all(
                        price, line.product_uom_qty, line.product_id,
                        repair.partner_id)
                    taxed += sum(x['amount'] for x in tax_calculate['taxes'])
            repair.amnt_untaxed = untaxed
            repair.amnt_tax = taxed
            repair.amnt_total = untaxed + taxed
            repair.operation_subtotal = operation_subtotal
            repair.fee_subtotal = fee_subtotal
            repair.real_hours_qty = real_hours_qty
            repair.real_hours_cost = real_hours_cost
            repair.cost_total = operation_subtotal + real_hours_cost
            repair.last_purchase_price_valued = last_cost_total

    @api.multi
    @api.depends('partner_id', 'partner_id.property_payment_term')
    def _compute_date_due(self):
        for repair in self:
            if repair.partner_id and repair.partner_id.property_payment_term:
                pterm_list = repair.partner_id.property_payment_term.compute(
                    value=1, date_ref=False)[0]
                if pterm_list:
                    repair.date_due = max(line[0] for line in pterm_list)
            else:
                repair.date_due = fields.Date.from_string(fields.Date.today())

    @api.multi
    def _compute_create_date2(self):
        for repair in self:
            repair.create_date2 = fields.Datetime.from_string(
                repair.create_date).strftime('%Y-%m-%d')

    @api.multi
    def _compute_bez(self):
        for repair in self:
            for line in repair.operations.filtered(lambda x: x.to_invoice):
                if line.tax_id:
                    for tax in line.tax_id:
                        repair.bez = tax.amount * 100

    @api.multi
    def _get_general_conditions(self):
        return self.env.user.company_id.general_conditions

    @api.multi
    def _get_general_conditions_cas(self):
        return self.env.user.company_id.general_conditions_cas

    name = fields.Char(default='/')
    amnt_untaxed = fields.Float(string='Untaxed Amount',
                                compute='_compute_repair_amount', store=True)
    amnt_tax = fields.Float(string='Taxes', compute='_compute_repair_amount',
                            store=True)
    amnt_total = fields.Float(string='Total', compute='_compute_repair_amount',
                              store=True)
    date_due = fields.Date(compute='_compute_date_due')
    create_date2 = fields.Char(compute='_compute_create_date2')
    bez = fields.Float(
        string="BEZ", compute='_compute_bez', digits=(3, 2))
    general_conditions = fields.Html(
        string='General conditions in Basque',
        default=_get_general_conditions)
    general_conditions_cas = fields.Html(
        string='General conditions in Spanish',
        default=_get_general_conditions_cas)
    photo1 = fields.Binary(string='Photo 1')
    photo2 = fields.Binary(string='Photo 2')
    photo3 = fields.Binary(string='Photo 3')
    photo4 = fields.Binary(string='Photo 4')
    estimated_hours = fields.Float(string='Estimated Hours')
    cost_total = fields.Float(string='Cost Total',
                              compute='_compute_repair_amount', store=True)
    operation_subtotal = fields.Float(string='Material Cost',
                                      compute='_compute_repair_amount',
                                      store=True)
    fee_subtotal = fields.Float(string='Fee Cost',
                                compute='_compute_repair_amount', store=True)
    real_hours_cost = fields.Float(
        string='Real Hours Cost', compute='_compute_repair_amount', store=True)
    real_hours_qty = fields.Float(
        string='Real Hours Qty', compute='_compute_repair_amount', store=True)
    product_id = fields.Many2one(states={'draft': [('readonly', False)],
                                         'confirmed': [('readonly', False)],
                                         'under_repair': [('readonly', False)],
                                         '2binvoiced': [('readonly', False)]})
    quotation_notes = fields.Html(
        string='Quotation Notes', default=_defaul_quotation_notes)
    last_purchase_price_valued = fields.Float(
        string='Last Purchase Price Valued', compute='_compute_repair_amount',
        store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).create(vals)

    @api.multi
    def write(self, vals):
        result = super(MrpRepair, self).write(vals)
        if 'end_date' in vals and vals.get('end_date', False):
            for repair in self:
                cond = [('origin', '=', repair.name)]
                moves = self.env['stock.move'].search(cond)
                if moves:
                    moves.write({'date': vals.get('end_date')})
                    for move in moves:
                        my_date = fields.Datetime.from_string(move.date)
                        today = fields.Datetime.from_string(
                            fields.Datetime.now())
                        my_date = my_date.replace(
                            hour=today.hour, minute=today.minute)
                        move.write({'date': my_date})
        if 'invoice_id' in vals and vals.get('invoice_id', False):
            for repair in self.filtered(
                    lambda x: x.company_id and
                        x.company_id.note_for_out_invoice):
                repair.invoice_id.notes = (
                    repair.company_id.note_for_out_invoice)
        return result

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.env['ir.sequence'].get('mrp.repair')
        return super(MrpRepair, self).copy(default)

    @api.multi
    def action_show_purchase_order(self):
        self.ensure_one()
        self = self.with_context(
            default_repair_analytic_id=self.analytic_account.id)
        purchase_ids = self.env['purchase.order.line'].search(
            [('repair_id', '=', self.id)]).mapped('order_id').ids
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,graph,calendar',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'purchase.view_purchase_order_filter').id,
            'domain': "[('id','in',{})]".format(purchase_ids),
            'context': self.env.context
            }

    @api.multi
    def action_show_account_invoice(self):
        self.ensure_one()
        self = self.with_context(
            default_repair_analytic_id=self.analytic_account.id,
            default_type='in_invoice', type='in_invoice',
            journal_type='purchase')
        invoice_ids = self.env['account.invoice.line'].search(
            [('repair_id', '=', self.id)]).mapped('invoice_id').ids
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,calendar,graph',
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'account.view_account_invoice_filter').id,
            'domain': "[('id','in',{})]".format(invoice_ids),
            'context': self.env.context
            }

    @api.multi
    def action_show_purchase_order_lines(self):
        self.ensure_one()
        self = self.with_context(
            default_account_analytic_id=self.analytic_account.id,
            default_repair_id=self.id)
        purchase_line_ids = self.env['purchase.order.line'].search(
            [('repair_id', '=', self.id)]).ids
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order.line',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'purchase.view_purchase_order_filter').id,
            'domain': "[('id','in',{})]".format(purchase_line_ids),
            'context': self.env.context
            }

    @api.multi
    def action_show_account_invoice_lines(self):
        self.ensure_one()
        self = self.with_context(
            default_account_analytic_id=self.analytic_account.id,
            default_repair_id=self.id)
        invoice_line_ids = self.env['account.invoice.line'].search(
            [('repair_id', '=', self.id)]).ids
        return {
            'view_type': 'form',
            'view_mode': 'tree,form,calendar,graph',
            'res_model': 'account.invoice.line',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'account.view_account_invoice_filter').id,
            'domain': "[('id','in',{})]".format(invoice_line_ids),
            'context': self.env.context
            }

    @api.multi
    def action_open_related_fees(self):
        result = self.env.ref(
            'mrp_repair_fee.action_mrp_repair_fee').read()[0]
        result['domain'] = "[('repair_id', 'in'," +\
            str(self.ids) + ")]"
        result['context'] = "{}"
        return result

    @api.multi
    def action_open_related_lines(self):
        result = self.env.ref(
            'astikar_custom.action_mrp_repair_line').read()[0]
        result['domain'] = "[('repair_id', 'in'," +\
            str(self.ids) + ")]"
        return result


class MrpRepairLine(models.Model):
    _inherit = 'mrp.repair.line'

    @api.multi
    def write(self, vals):
        if 'product_uom_qty'in vals:
            vals['load_cost'] = bool(vals.get('product_uom_qty', 0.0))
        return super(MrpRepairLine, self).write(vals)

    @api.model
    def create(self, vals):
        vals['load_cost'] = bool(vals.get('product_uom_qty', 0.0))
        return super(MrpRepairLine, self).create(vals)

    @api.multi
    @api.depends('product_id', 'product_id.qty_available',
                 'product_id.repair_product_count')
    def _compute_available_qty(self):
        for line in self.filtered(lambda l: l.type == 'add' and not l.move_id):
            line.available_qty = (
                line.product_id.qty_available -
                line.product_id.repair_product_count)

    @api.depends('last_purchase_price', 'product_uom_qty',)
    def _compute_get_purchase_valued(self):
        for record in self:
            total = 0
            if record.last_purchase_price and record.product_uom_qty:
                total = record.last_purchase_price * record.product_uom_qty
            record.last_purchase_price_valued = total

    available_qty = fields.Float(
        string='Available Qty', compute='_compute_available_qty',
        digits=dp.get_precision('Product Unit of Measure'))
    product_uom_qty = fields.Float(
        digits=dp.get_precision('Product Price'))
    expected_qty = fields.Float(
        digits=dp.get_precision('Product Price'))
    last_purchase_price = fields.Float(
        string='Last Purchase Price',
        related='product_id.last_purchase_price', readonly=True)
    last_purchase_price_valued = fields.Float(
        string='Last Purchase Price Valued',
        compute='_compute_get_purchase_valued',
        store=True, digits=dp.get_precision('Product Price'))


class MrpRepairFee(models.Model):
    _inherit = 'mrp.repair.fee'

    is_from_menu = fields.Boolean(string='Created from menu', default=False)

    @api.model
    def create(self, vals):
        vals['load_cost'] = not vals.get('to_invoice', False)
        return super(MrpRepairFee, self).create(vals)
