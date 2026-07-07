# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import os

from odoo import _, api, exceptions, fields, models


class DocuInspecTrafosVer(models.TransientModel):
    _name = "docu.inspec.trafos.ver"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        [("choose", "choose"), ("get", "get")],  # choose language or get the file
        default="choose",
    )
    docu = fields.Char(string="Documento")
    carpeta = fields.Char()

    @api.model
    def default_get(self, var_fields):
        result = super().default_get(var_fields)
        result.update({"state": "choose", "data": "", "name": ""})
        return result

    def ver_docu_inspec_trafos(self):
        if not self.carpeta:
            return
        if self.docu:
            w_docu = self.docu
        # Obtiene en mayusculas el campo w_docu
        w_docu = w_docu.strip()
        w_dir = "/media/" + self.carpeta.strip()
        if not w_docu:
            raise exceptions.Warning(_("No se ha encontrado el documento"))
        this = self[0]
        fichero_name = self.buscar_dto(w_dir, w_docu)
        if not fichero_name:
            raise exceptions.Warning(_("No se ha encontrado el documento"))
        #       fname = "docu.pdf"   #rodrigo
        docudata = w_docu.split(".")
        if not (len(docudata) > 1):
            w_docu = w_docu + ".pdf"
        fname = w_docu  # rodrigo"
        fichero_salida = fichero_name
        file_point = open(fichero_salida, "rb")
        file_data = base64.b64encode(file_point.read())
        file_point.close()
        this.write({"state": "get", "data": file_data, "name": fname})
        return {
            "type": "ir.actions.act_window",
            "res_model": "docu.inspec.trafos.ver",
            "view_mode": "form",
            "view_type": "form",
            "res_id": this.id,
            "views": [(False, "form")],
            "target": "new",
        }

    def buscar_dto(self, directorio, docu):
        if not os.path.isdir(directorio):
            raise exceptions.Warning(_("No se encuentra la carpeta %s") % directorio)
        docudata = docu.strip().split(".")
        if not (len(docudata) > 1):
            docu = docu + ".pdf"
        for root, _directorio, ficheros in os.walk(directorio):
            for fichero in ficheros:
                if docu == fichero:
                    return root + "/" + fichero
        return False
