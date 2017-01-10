# -*- coding: utf-8 -*-
# Copyright 2016 Alfredo de la Fuente - AvanzOSC
# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    no_sexual_offenses = fields.Boolean(
        string='Negative certificate sexual offenses', default=True,
        help='If check is selected it means that the employee has a '
        'negative certificate of sexual offenses.')
    no_sexual_offenses_certificate = fields.Char(
        string='Certificate Verification Code',
        help='With this code you can validate the certificate.')
    no_sexual_offenses_certificate_date = fields.Date(
        string='Certificate Date')
    certificate_link = fields.Char(
        string='Certificate Validation Link',
        compute='_compute_certificate_link')

    @api.depends('identification_id')
    def _compute_certificate_link(self):
        for record in self:
            record.certificate_link =\
                'https://sede.mjusticia.gob.es/verificaCSV/'\
                'FormularioVerificacion'
            if record.identification_id:
                record.certificate_link = '{}?documento={}'.format(
                    record.certificate_link, record.identification_id)
