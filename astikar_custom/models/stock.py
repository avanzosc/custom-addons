# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields, tools
from openerp.addons import decimal_precision as dp


class StockHistory(models.Model):
    _inherit = 'stock.history'

    product_type = fields.Selection(
        [('product', 'Stockable Product'), ('consu', 'Consumable'),
         ('service', 'Service')], string='Product Type')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'stock_history')
        cr.execute("""
        CREATE OR REPLACE VIEW stock_history AS (
            SELECT MIN(id) as id,
                move_id,
                location_id,
                company_id,
                product_id,
                product_categ_id,
                SUM(quantity) as quantity,
                date,
                COALESCE(SUM(price_unit_on_quant * quantity) /
                        NULLIF(SUM(quantity), 0), 0) as price_unit_on_quant,
                source, product_type
                FROM
                ((SELECT
                    stock_move.id AS id,
                    stock_move.id AS move_id,
                    dest_location.id AS location_id,
                    dest_location.company_id AS company_id,
                    stock_move.product_id AS product_id,
                    product_template.categ_id AS product_categ_id,
                    quant.qty AS quantity,
                    stock_move.date AS date,
                    quant.cost as price_unit_on_quant,
                    stock_move.origin AS source,
                    product_template.type AS product_type
                FROM
                    stock_move
                JOIN
                    stock_quant_move_rel on
                        stock_quant_move_rel.move_id = stock_move.id
                JOIN
                    stock_quant as quant on
                        stock_quant_move_rel.quant_id = quant.id
                JOIN
                   stock_location dest_location ON
                       stock_move.location_dest_id = dest_location.id
                JOIN
                    stock_location source_location ON
                        stock_move.location_id = source_location.id
                JOIN
                    product_product ON
                        product_product.id = stock_move.product_id
                JOIN
                    product_template ON
                        product_template.id = product_product.product_tmpl_id
                WHERE (quant.qty>0 AND stock_move.state = 'done' AND
                       dest_location.usage in ('internal', 'transit'))
                  AND (
                    not (source_location.company_id is null and
                        dest_location.company_id is null) or
                    source_location.company_id != dest_location.company_id or
                    source_location.usage not in ('internal', 'transit'))
                ) UNION ALL
                (SELECT
                    (-1) * stock_move.id AS id,
                    stock_move.id AS move_id,
                    source_location.id AS location_id,
                    source_location.company_id AS company_id,
                    stock_move.product_id AS product_id,
                    product_template.categ_id AS product_categ_id,
                    - quant.qty AS quantity,
                    stock_move.date AS date,
                    quant.cost as price_unit_on_quant,
                    stock_move.origin AS source,
                    product_template.type AS product_type
                FROM
                    stock_move
                JOIN
                    stock_quant_move_rel on
                        stock_quant_move_rel.move_id = stock_move.id
                JOIN
                    stock_quant as quant on
                        stock_quant_move_rel.quant_id = quant.id
                JOIN
                    stock_location source_location ON
                        stock_move.location_id = source_location.id
                JOIN
                    stock_location dest_location ON
                        stock_move.location_dest_id = dest_location.id
                JOIN
                    product_product ON
                        product_product.id = stock_move.product_id
                JOIN
                    product_template ON
                        product_template.id = product_product.product_tmpl_id
                WHERE (quant.qty>0 AND stock_move.state = 'done' AND
                       source_location.usage in ('internal', 'transit'))
                 AND (
                    not (dest_location.company_id is null
                    and source_location.company_id is null) or
                    dest_location.company_id != source_location.company_id or
                    dest_location.usage not in ('internal', 'transit'))
                ))
                AS foo
                GROUP BY move_id, location_id, company_id, product_id,
                product_categ_id, date, source, product_type
            )""")


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    @api.depends("product_id", "product_id.standard_price", "qty")
    def _compute_standard_value(self):
        for record in self:
            record.standard_value = (record.product_id.standard_price *
                                     record.qty)

    standard_value = fields.Float(
        string="Standard Value", store=True, compute="_compute_standard_value",
        digits=dp.get_precision('Product Price'))
    product_tmpl_id = fields.Many2one(
        string='Product template', comodel_name='product.template',
        related='product_id.product_tmpl_id', store=True)
    categ_id = fields.Many2one(
        related='product_tmpl_id.categ_id', store=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def do_transfer(self):
        res = super(StockPicking, self).do_transfer()
        repair_obj = self.env['mrp.repair']
        repair_line_obj = self.env['mrp.repair.line']
        for picking in self.filtered(
                lambda x: x.picking_type_id.code == 'incoming'):
            for move_line in picking.move_lines.filtered(
                    'purchase_line_id.account_analytic_id'):
                repair = repair_obj.search(
                    [('analytic_account', '=',
                      move_line.purchase_line_id.account_analytic_id.id),
                     ('state', 'not in', ('cancel', 'done'))])
                if repair and move_line.product_id.type != 'service':
                    line_values = repair_line_obj.product_id_change(
                        repair[0].pricelist_id.id, move_line.product_id.id,
                        uom=move_line.product_uom.id,
                        partner_id=move_line.purchase_line_id.partner_id.id
                        )['value']
                    line_values.update(repair_line_obj.onchange_operation_type(
                        'add', repair.guarantee_limit)['value'])
                    line_values.update({
                        'product_id': move_line.product_id.id,
                        'repair_id': repair[0].id,
                        'user_id': self.env.user.id,
                        'type': 'add',
                        'product_uom_qty': move_line.product_uom_qty,
                        'expected_qty': move_line.product_uom_qty,
                        'tax_id': [(6, 0, 'tax_id' in line_values and
                                    line_values['tax_id'] or [])],
                    })
                    repair_line_obj.create(line_values)
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        res = super(StockMove, self)._get_invoice_line_vals(move, partner,
                                                            inv_type)
        if move.purchase_line_id.repair_id:
            res['repair_id'] = move.purchase_line_id.repair_id.id
        return res


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    quant_excel_file_data = fields.Binary('File')
    quant_excel_file_name = fields.Char('Filename')
