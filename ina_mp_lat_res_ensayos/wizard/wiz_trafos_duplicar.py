# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, exceptions, fields, models


class WizTrafosDuplicar(models.TransientModel):
    _name = "wiz.trafos.duplicar"
    _description = "Duplicar Trafo"

    num_serie = fields.Float(string="Numero de Serie", digits=(15, 0))

    def action_duplica_trafo(self):
        active_ids = self.env.context.get("active_ids", [])
        if len(active_ids) > 1:
            raise exceptions.Warning(_("Debes marcar solamente 1 Trafo para Duplicar."))
        dup_ids = self.env["res.trafos"].browse(self.env.context.get("active_ids"))
        for r in dup_ids:
            w_name = self.num_serie
            w_int = int(self.num_serie)
            w_numero = str(w_int)
            nuevo_trafo_id = r.copy(
                default={
                    "name": w_name,
                    "num_serie": w_numero,
                }
            ).id
            for v in dup_ids.lineas_rela_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
            for v in dup_ids.lineas_vacio_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
            for v in dup_ids.lineas_corto_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
            for v in dup_ids.lineas_dielectrico_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
            for v in dup_ids.lineas_resultados_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
            for v in dup_ids.lineas_equipos_ids:
                v.copy(default={"trafo_id": nuevo_trafo_id, "num_serie": w_numero})
