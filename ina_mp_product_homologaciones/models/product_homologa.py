# Copyright 2015 Guewen Baconnier
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2016 Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    homologa_ids = fields.One2many(
        comodel_name="product.homologa", inverse_name="product_tmpl_id", copy=False
    )


class ProductCia(models.Model):
    _name = "product.cia"
    _description = "Compañias Electricas"

    name = fields.Char("Compañia")


class ProductHomologa(models.Model):
    _name = "product.homologa"
    _description = "Homologacion de Productos"

    cia = fields.Many2one(comodel_name="product.cia", string="Compañia")
    product_id = fields.Many2one(comodel_name="product.product", string="Producto")
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Plantilla",
        related="product_id.product_tmpl_id",
    )
    categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Categoria",
        related="product_id.categ_id",
        store=True,
    )
    tipo_plano = fields.Selection(
        [
            ("prov", "Proveedor"),
            ("clien", "Cliente"),
        ],
        default="prov",
    )
    plano = fields.Char(related="product_id.plano")
    plano_cliente = fields.Char("Plano Cliente", related="product_id.plano_cliente")
    planilla = fields.Char(related="product_id.planilla")
    manu_instru = fields.Char("Manual Inst.", related="product_id.manu_instru")
    cod_cia = fields.Char("Cod. Producto Cia")
    den_cia = fields.Char("Denominacion Cia")
    nor_cia = fields.Char("Norma Cia")

    def action_ver_ficha(self):
        self.ensure_one()
        return {
            "name": _("Ficha de Producto"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "product.template",
            "res_id": self.product_tmpl_id.id,
        }
