# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.depends('order_line', 'order_line.tasks', 'state')
    def _compute_task_exists(self):
        for record in self:
            task_lst = record.order_line.mapped('tasks.id')
            if not task_lst:
                record.task_exists = False
            else:
                record.task_exists = True

    @api.depends('procurement_group_id',
                 'procurement_group_id.procurement_ids',
                 'procurement_group_id.procurement_ids.state')
    @api.multi
    def _compute_get_shipped(self):
        for sale in self:
            group = sale.procurement_group_id
            val = False
            if group:
                val = all([proc.state in ['cancel', 'done'] for proc in
                           group.procurement_ids])
            sale.shipped = val

    @api.multi
    def _default_sale_note(self):
        return self.env.user.company_id.sale_note_report

    requested_date = fields.Datetime(readonly=False)
    commitment2_date = fields.Datetime(
        string="Commitment Date",
        help="Date by which the products are sure to be delivered. This is "
             "a date that you can promise to the customer, based on the "
             "Product Lead Times.", default=fields.Date.today())
    task_exists = fields.Boolean('Task Exists', compute="_compute_task_exists",
                                 store=True)
    shipped = fields.Boolean(compute='_compute_get_shipped',
                             string='Delivered', store=True)
    show_sale_note = fields.Boolean()
    sale_note = fields.Text(default=_default_sale_note)
    active = fields.Boolean(string='Active', default=True)

    @api.multi
    def action_view_task(self):
        self.ensure_one()
        task_obj = self.env['project.task']
        task_lst = task_obj.search([('sale_line_id.order_id', '=', self.id)])
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_id': task_lst.id or False,
            'res_model': 'project.task',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': "[('id','in',["+','.join(map(str, task_lst.ids))+"])]",
            }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tasks = fields.One2many('project.task', 'sale_line_id', 'Tasks')
