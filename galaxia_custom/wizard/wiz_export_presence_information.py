# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons.event_track_assistant._common import\
    _convert_to_local_date
import base64
import StringIO
import logging
_logger = logging.getLogger(__name__)
try:
    import pyExcelerator as xl
except (ImportError, IOError) as err:
    _logger.debug(err)


class WizExportPresenceInformation(models.TransientModel):
    _name = 'wiz.export.presence.information'
    _description = 'Wizard for export presences information'

    @api.multi
    def export_profit(self, sheet1):
        presence_obj = self.env['event.track.presence']
        boldFont = xl.Font()
        boldFont.bold = True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14 = xl.Font()
        boldFont14.bold = True
        boldFont14.height = 220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        sheet1.write(0, 0, 'CLIENTE', boldS14)
        sheet1.write(0, 1, 'DIRECCION', boldS14)
        sheet1.write(0, 2, 'DIA', boldS14)
        sheet1.write(0, 3, 'FECHA Y HORA', boldS14)
        line = 1
        for p in presence_obj.browse(self.env.context.get('active_ids')):
            line += 1
            partner = p.event.sale_order.partner_shipping_id
            sheet1.write(line, 0, partner.name)
            address = u"\n{} {} {}".format(
                partner.street or '', partner.street2 or '',
                partner.city or '')
            sheet1.write(line, 1, address)
            if p.session_day == '0':
                day = 'Lunes'
            elif p.session_day == '1':
                day = 'Martes'
            elif p.session_day == '2':
                day = 'Miércoles'
            elif p.session_day == '3':
                day = 'Jueves'
            elif p.session_day == '4':
                day = 'Viernes'
            elif p.session_day == '5':
                day = 'Sábado'
            else:
                day = 'Domingo'
            sheet1.write(line, 2, day)
            session_date = fields.Datetime.to_string(_convert_to_local_date(
                p.session_date, self.env.user.tz))
            sheet1.write(line, 3, session_date)
        return sheet1

    @api.multi
    def export_csv(self):
        fileDoc = xl.Workbook()
        sheet1 = fileDoc.add_sheet("Informe presencias")
        sheet1 = self.export_profit(sheet1)
        fname = 'Informe_presencias' + '.xls'
        file = StringIO.StringIO()
        fileDoc.save(file)
        fileDocFin = base64.encodestring(file.getvalue())
        vals = {'csv_file': fileDocFin,
                'csv_fname': fname}
        wiz = self.env['wiz.export.csv'].create(vals)
        return {'type': 'ir.actions.act_window',
                'res_model': 'wiz.export.csv',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                }
