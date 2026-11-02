# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import os

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DocuRmaVer(models.TransientModel):
    _name = "docu.rma.ver"
    _description = "Ver documento RMA"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        selection=[("choose", "choose"), ("get", "get")],
        default="choose",
    )
    docu = fields.Char(string="Documento")
    carpeta = fields.Char()

    @api.model
    def default_get(self, var_fields):
        res = super().default_get(var_fields)
        res.update({"state": "choose", "data": False, "name": ""})
        return res

    def ver_docu_rma(self):
        if not self.carpeta or not self.docu:
            raise UserError(_("No se ha encontrado el documento"))

        w_docu = self.docu.strip()
        w_dir = "/media/" + self.carpeta.strip()

        fichero_name = self._buscar_dto(w_dir, w_docu)
        if not fichero_name:
            raise UserError(_("No se ha encontrado el documento"))

        if "." not in w_docu:
            w_docu = w_docu + ".pdf"

        with open(fichero_name, "rb") as f:
            file_data = base64.b64encode(f.read())

        self.write({"state": "get", "data": file_data, "name": w_docu})
        return {
            "type": "ir.actions.act_window",
            "res_model": "docu.rma.ver",
            "view_mode": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }

    def _buscar_dto(self, directorio, docu):
        if not os.path.isdir(directorio):
            raise UserError(_("No se encuentra la carpeta %s") % directorio)
        docu = docu.strip()
        if "." not in docu:
            docu = docu + ".pdf"
        for root, _dirs, ficheros in os.walk(directorio):
            for fichero in ficheros:
                if docu == fichero:
                    return os.path.join(root, fichero)
        return False
