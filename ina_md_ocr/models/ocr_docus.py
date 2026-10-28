# Copyright 2015 Guewen Baconnier
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2016 Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class OcrDocus(models.Model):
    _name = "ocr.docus"
    _description = "Documentos OCR"

    ocr_id = fields.Many2one(comodel_name="inael.ocr", string="OCR", ondelete="cascade")
    carpeta = fields.Text("Carpeta del fichero", default="/in/Documentacion/Ocr_Sintra")
    fichero = fields.Char("Documento")
    nota = fields.Text(copy=False)
