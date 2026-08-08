# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar", string="Puesto")
    motivo_rechazo = fields.Selection(
        selection=[
            ("no cumple plano", "No cumple plano"),
            ("pintura", "Pintura"),
            ("fallo de montaje interno", "Fallo de montaje interno"),
            ("rebabas", "Rebabas"),
            ("material obsoleto", "Material Obsoleto"),
            ("utillaje", "Utillaje"),
            ("rotura durante montaje", "Rotura durante montaje interno"),
            ("sobrantes", "Material Sobrante"),
            ("ensayos", "Ensayos"),
        ],
        string="Motivo",
        default="no cumple plano",
    )

    # --- Logica operativa comentada: solo referencia, no se ejecuta. ---

    # @api.onchange("puesto_id")
    # def _onchange_puesto_id(self):
    #     if self.puesto_id:
    #         self.location_id = self.puesto_id.location_id
    #         self.scrap_location_id = self.puesto_id.scrap_location_id
