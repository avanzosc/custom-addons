# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestRockboticCustom(common.TransactionCase):

    def setUp(self):
        super(TestRockboticCustom, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.invoice_model = self.env['account.invoice']
        self.ir_values_obj = self.env['ir.values']
        self.partner = self.browse_ref('base.res_partner_address_20')
        claim_vals = {'name': 'Rockbotic test',
                      'partner_id': self.partner.id}
        self.claim = self.claim_model.create(claim_vals)
        self.contract = self.env.ref('account.analytic_support_internal')
        self.contract.recurring_invoices = True
        self.comment = u'Testing ir value'
        self.ir_values_obj.set_default(
            'account.invoice', 'comment', self.comment)

    def test_rockbotic_custom(self):
        self.assertEqual(self.partner.claim_count, 1,
                         'Bad number of claims for partner')
        res = self.partner.show_crm_claims_from_partner()
        domain = "[('id', 'in', [{}])]".format(self.claim.id)
        self.assertNotIn(domain, res.get('domain', False),
                         'Bad domain in show_crm_claims_from_partner')

    def test_analytic_recurring(self):
        self.contract.recurring_create_invoice()
        invoice = self.invoice_model.search([
            ('origin', '=', self.contract.code)])
        self.assertEqual(invoice.comment, self.comment)
