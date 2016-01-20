# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestAstikarCustom(common.TransactionCase):

    def setUp(self):
        super(TestAstikarCustom, self).setUp()
        self.ir_sequence_model = self.env['ir.sequence']
        self.mrp_repair_model = self.env['mrp.repair']
        self.mrp_repair_sequence = self.ref('mrp_repair.seq_mrp_repair')

    def test_default_quotation_note(self):
        note = 'Test Sale Note'
        self.env.user.company_id.sale_note = note
        repair = self.mrp_repair_model.new(
            self.mrp_repair_model.default_get(['quotation_notes']))
        self.assertTrue(repair.quotation_notes)
        self.assertEqual(repair.quotation_notes,
                         self.env.user.company_id.sale_note)
        self.assertEqual(repair.quotation_notes,
                         note)

    def test_new_repair_sequence_assign(self):
        name = self._get_next_name()
        mrp_repair = self.mrp_repair_model.create({
            'name': 'Testing MRP repair name',
        })
        self.assertNotEqual(mrp_repair.name, '/')
        self.assertEqual(mrp_repair.name, name)

    def test_copy_repair_sequence_assign(self):
        name = self._get_next_name()
        mrp_repair = self.mrp_repair_model.create({
            'name': 'Testing MRP repair name',
        })
        mrp_repair_copy = mrp_repair.copy()
        self.assertNotEqual(mrp_repair_copy.name, mrp_repair.name)
        self.assertEqual(mrp_repair_copy.name, name)

    def _get_next_name(self):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(
            self.mrp_repair_sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(
            self.mrp_repair_sequence.suffix, d)
        name = (prefix + ('%%0%sd' % self.mrp_repair_sequence.padding %
                          self.mrp_repair_sequence.number_next_actual) +
                suffix)
        return name
