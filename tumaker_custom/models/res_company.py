# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    rml_footer = fields.Text(translate=True)
    sale_note_report = fields.Text()
    out_picking_gdpr_eus = fields.Text(
        string='Out pickings in basque', translate=True)
    in_picking_gdpr_eus = fields.Text(
        string='In pickings in basque', translate=True)
    out_invoice_gdpr_eus = fields.Text(
        string='Out invoices in basque', translate=True)
    in_invoice_gdpr_eus = fields.Text(
        string='In invoices in basque', translate=True)
