# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import os

from odoo import api, fields, models


class TrafosInspeDocus(models.Model):
    _name = "trafos.inspec.docus"

    @api.depends("fichero")
    def _compute_existe_fichero(self):
        for r in self:
            r.existe_fichero = bool(r.ver_docu_inspec_trafos())

    trafo_id = fields.Many2one(
        string="Inspeccion Trafos", comodel_name="res.trafos", ondelete="cascade"
    )
    carpeta = fields.Text(
        string="Carpeta del fichero",
        default="/in/Documentacion/Documentacion_Inspeccion_Trafos",
    )  # Preguntar
    fichero = fields.Char(string="Documento")
    existe_fichero = fields.Boolean(
        string="Fichero Encontrado", compute="_compute_existe_fichero"
    )
    nota = fields.Text(copy=False)

    def action_ver_docu(self):
        ver_obj = self.env["docu.inspec.trafos.ver"]
        # Me aseguro que tenga registro la tabla de wizard
        id_obj1 = ver_obj.search([("id", ">=", 0)], limit=1)  # traduzco al id como id
        if not id_obj1:
            val = {}
            obj_id = ver_obj.create(val)  # devuelve el id como entero
        else:
            obj_id = id_obj1[0]
        id_obj1 = ver_obj.search([("id", ">=", 0)], limit=1)  # traduzco al id como id
        obj_id = id_obj1[0]
        obj_id.write({"docu": self.fichero, "carpeta": self.carpeta})
        fichero = obj_id.ver_docu_inspec_trafos()
        return fichero

    def ver_docu_inspec_trafos(self):
        if not self.fichero:
            return False
        fichero_name = self.buscar_dto()
        if not fichero_name:
            return False  # NO Encontrado, vuelvo
        return True

    def buscar_dto(self):
        docu = self.fichero.strip()
        docudata = docu.split(".")
        if not (len(docudata) > 1):
            docu = docu + ".pdf"
        directorio = "/media" + self.carpeta.strip()
        if not os.path.isdir(directorio):
            return False
        for root, _directorios, ficheros in os.walk(directorio):
            for fichero in ficheros:
                if docu == fichero:
                    return root + "/" + fichero
        return False

    def buscar_dto_viejo(self):
        docu = self.fichero.strip() + ".pdf"
        directorio = "/media" + self.carpeta.strip()
        if not os.path.isdir(directorio):
            return False
        for root, _directorios, ficheros in os.walk(directorio):
            pdfs = [fila for fila in ficheros if fila.endswith(".pdf")]
            for fichero in pdfs:
                if docu == fichero:
                    return root + "/" + fichero
        return False
