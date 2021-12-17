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

    @api.multi
    @api.depends('product_id', 'qty',)
    def _compute_get_purchase_valued(self):
        for record in self:
            total = 0
            if record.product_id and record.qty:
                total = record.product_id.last_purchase_price * record.qty
            record.last_purchase_price_valued = total

    standard_value = fields.Float(
        string="Standard Value", store=True, compute="_compute_standard_value",
        digits=dp.get_precision('Product Price'))
    last_purchase_price_valued = fields.Float(
        string='Last Purchase Price Valued',
        compute='_compute_get_purchase_valued',
        store=True, digits=dp.get_precision('Product Price'))
    categ_id = fields.Many2one(related='product_id.categ_id', store=True)
    product_tmpl_id = fields.Many2one(
        string='Product template', comodel_name='product.template',
        related='product_id.product_tmpl_id', store=True)

    @api.model
    def _quant_create(self, qty, move, lot_id=False, owner_id=False,
                      src_package_id=False, dest_package_id=False,
                      force_location_from=False, force_location_to=False):
        quant = super(StockQuant, self)._quant_create(
            qty, move, lot_id=lot_id, owner_id=owner_id,
            src_package_id=src_package_id, dest_package_id=dest_package_id,
            force_location_from=force_location_from,
            force_location_to=force_location_to)
        if (move.picking_id and move.picking_id.picking_type_id and
                move.picking_id.picking_type_id.code == 'incoming'):
            quant.in_date = move.picking_id.date
        return quant
