# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class InaelOcrLine(models.Model):
    _name = "inael.ocr.line"
    _description = "Lineas OCR"

    ocr_id = fields.Many2one(
        comodel_name="inael.ocr", string="Objetivo", ondelete="cascade"
    )
    pedido = fields.Char()
    sale_id = fields.Many2one(comodel_name="sale.order", string="Orden Venta")
    integracion = fields.Char()
    descri = fields.Char("Descripcion")
    cod_ib = fields.Char("Cod IB")
    product_id = fields.Many2one(comodel_name="product.product", string="Producto")
    fecha_entrega_ib = fields.Datetime("Fecha Entrega IB")
    fecha_entrega_inael = fields.Datetime(
        "Fecha Planificada", related="ocr_id.fecha_planificada"
    )
    instalador = fields.Text()
    resp_ib = fields.Char("Resp. IB")
    sim = fields.Char()
    nota = fields.Char()
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("cancel", "Cancelado"),
            ("pendi", "Pte. Comercial"),
            ("sinplan", "Sin Planificar"),
            ("plan", "Planificado"),
            ("envi", "Enviado"),
            ("done", "Recepcionado"),
        ],
        default="draft",
        string="Estado",
        copy=False,
    )
