# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class InaelOcr(models.Model):
    _name = "inael.ocr"
    _description = "Gestion OCRs de Iberdrola"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Objetivo", required=True, copy=False)
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
    matricula = fields.Char()
    obra = fields.Char()
    codigo_inst = fields.Char("Codigo Instalacion")
    instalacion = fields.Text()
    caracteristicas = fields.Char()
    fecha_entrega = fields.Datetime()
    nota = fields.Text("Observaciones")
    line_ocr_ids = fields.One2many(
        comodel_name="inael.ocr.line",
        inverse_name="ocr_id",
        string="Datos OCRs",
        copy=True,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente")
    proyecto = fields.Char(copy=False)
    fecha_planificada = fields.Datetime()
    zona = fields.Selection(
        selection=[
            ("1-N", "1-Norte"),
            ("2-O", "2-Oeste"),
            ("4-E", "4-Este"),
            ("5-C", "5-Centro"),
        ],
        default="1-N",
        string="Region",
    )
    mail_enviado_a_ventas = fields.Boolean("eMail enviado", default=False)
    purchase_id = fields.Many2one(
        comodel_name="purchase.order", string="OC Armario", copy=False
    )
    zona2 = fields.Char("Zona")
    utd = fields.Char("UTD")
    line_documen_ids = fields.One2many(
        comodel_name="ocr.docus",
        inverse_name="ocr_id",
        string="Documentos",
        copy=True,
    )

    _sql_constraints = [
        (
            "inael_ocr_unique_code",
            "UNIQUE (name)",
            "El Objetivo debe ser unico y parece que ya existe!",
        ),
    ]
