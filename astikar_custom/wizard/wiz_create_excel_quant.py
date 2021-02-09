# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import StringIO
import base64
try:
    import xlwt
except ImportError:
    xlwt = None


class WizCreateExcelQuant(models.TransientModel):
    _name = 'wiz.create.excel.quant'

    @api.multi
    def button_create_excel(self):
        self.ensure_one()
        book = xlwt.Workbook()
        file = StringIO.StringIO()
        cols = [u"Producto", u"Cantidad", u"Valor del inventario",
                u"Standard value"]
        sheet1 = book.add_sheet('Wave')
        row_index = 0
        row = sheet1.row(row_index)
        style0 = xlwt.easyxf(
            'font: name Times New Roman, colour blue, bold on')
        for row_i, col in enumerate(cols):
            row.write(row_i, col, style0)
        row_index += 1
        row = sheet1.row(row_index)
        products = {}
        quants = self.env['stock.quant'].browse(
            self.env.context.get('active_ids'))
        for quant in quants:
            name = quant.product_id.name
            if quant.product_id.default_code:
                name = u'[{}] {}'.format(quant.product_id.default_code, name)
            if name not in products:
                vals = {'qty': quant.qty,
                        'inventory_value': quant.inventory_value,
                        'standard_value': quant.standard_value}
                products[name] = vals
            else:
                q = quant.qty + products.get(name).get('qty')
                products[name]['qty'] = q
                i = quant.inventory_value + products.get(
                    name).get('inventory_value')
                products[name]['inventory_value'] = i
                i = quant.standard_value + products.get(
                    name).get('standard_value')
                products[name]['standard_value'] = i
        my_products = dict.fromkeys(products)
        for product in my_products:
            row.write(0, product or '')
            row.write(1, products[product].get('qty'))
            row.write(2, products[product].get('inventory_value'))
            row.write(3, products[product].get('standard_value'))
            row_index += 1
            row = sheet1.row(row_index)
        book.save(file)
        cond = [('company_id', '=', self.env.user.company_id.id)]
        warehouses = self.env['stock.warehouse'].search(cond)
        if warehouses:
            warehouses.write(
                {'quant_excel_file_data': base64.encodestring(file.getvalue()),
                 'quant_excel_file_name':
                 u'quants-{}.xls'.format(fields.Datetime.now())})
