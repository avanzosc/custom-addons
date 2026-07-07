# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, exceptions, fields, models


class WizCeldaresDuplicar(models.TransientModel):
    _name = "wiz.celdares.duplicar"
    _description = "Duplicar Celda"

    plano = fields.Char()

    def action_duplica_celda(self):
        active_ids = self.env.context.get("active_ids", [])
        if len(active_ids) > 1:
            raise exceptions.Warning(_("Debes marcar solamente 1 Celda para Duplicar."))
        dup_ids = self.env["res.celdas"].browse(self.env.context.get("active_ids"))
        for r in dup_ids:
            numero = r.name
            nueva_celda_id = r.copy(
                default={
                    "name": numero,
                }
            ).id
            for v in dup_ids.lineas_ids:
                v.copy(
                    default={
                        "celda_id": nueva_celda_id,
                    }
                )
