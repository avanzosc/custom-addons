# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestGalaxiaCustom(common.TransactionCase):

    def setUp(self):
        super(TestGalaxiaCustom, self).setUp()
        self.registration_model = self.env['event.registration']
        self.account_model = self.env['account.analytic.account']
        self.project_model = self.env['project.project']
        self.sale_model = self.env['sale.order']
        self.event_model = self.env['event.event']
        self.wiz_add_model = self.env['wiz.event.append.assistant']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-01-15',
                        'date': '2016-02-28'}
        self.account = self.account_model.create(account_vals)
        project_vals = {'name': 'project 1',
                        'analytic_account_id': self.account.id}
        self.project = self.project_model.create(project_vals)
        service_product = self.env.ref('product.product_product_consultant')
        service_product.write({'performance': 5.0,
                               'recurring_service': True})
        service_product.performance = 5.0
        service_product.route_ids = [
            (6, 0,
             [self.ref('procurement_service_project.route_serv_project')])]
        sale_vals = {
            'name': 'sale order 1',
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id': self.account.id,
            'project_by_task': 'no'}
        sale_line_vals = {
            'product_tmpl_id': service_product.id,
            'product_type': False,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price,
            'performance': 5.0,
            'january': True,
            'february': True,
            'week4': True,
            'week5': True,
            'tuesday': True,
            'thursday': True}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        self.env['marketing.config.settings'].create(
            {'module_marketing_campaign': False,
             'module_mass_mailing': False,
             'module_crm_profiling': False,
             'module_marketing_campaign_crm_demo': False,
             'show_all_customers_in_presences': True})
        self.env['ir.config_parameter'].create({
            'key': 'show.all.customers.in.presences',
            'value': True})

    def test_galaxia_custom(self):
        self.sale_order.action_button_confirm()
        self.sale_order.order_line[0]._compute_product_type()
        self.assertNotEqual(len(self.sale_order.order_line), 0,
                            'Sale order withour lines')
        cond = [('sale_order', '=', self.sale_order.id)]
        event = self.event_model.search(cond, limit=1)[:1]
        registration_vals = {
            'event_id': event.id,
            'partner_id': self.partner.id,
            'date_start': '2016-01-15 15:00:00',
            'date_end': '2016-02-28 18:00:00'}
        registration = self.registration_model.create(registration_vals)
        dict_add_wiz = registration.button_registration_open()
        add_wiz = self.wiz_add_model.with_context(
            active_ids=event.ids).browse(dict_add_wiz.get('res_id'))
        add_wiz.action_append()
        session = event.track_ids[0]
        session.presences[0]._compute_allowed_partner_ids()
        self.assertEqual(len(session.allowed_partner_ids),
                         len(session.presences[0].allowed_partner_ids),
                         'Bad allowed partners')
