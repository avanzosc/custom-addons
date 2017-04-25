# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestRockboticCustom(common.TransactionCase):

    def setUp(self):
        super(TestRockboticCustom, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.partner = self.browse_ref('base.res_partner_address_20')
        claim_vals = {'name': 'Rockbotic test',
                      'partner_id': self.partner.id}
        self.claim = self.claim_model.create(claim_vals)

    def test_rockbotic_custom(self):
        self.assertEqual(self.partner.claim_count, 1,
                         'Bad number of claims for partner')
        res = self.partner.show_crm_claims_from_partner()
        domain = "[('id', 'in', [{}])]".format(self.claim.id)
        self.assertNotIn(domain, res.get('domain', False),
                         'Bad domain in show_crm_claims_from_partner')
