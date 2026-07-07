# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import os

from odoo import api, fields, models


class MrpRepairDocu(models.Model):
    _name = "mrp.repair.docu"
    _description = "Documentos en Reparaciones"

    @api.depends("fichero")
    def _compute_existe_fichero(self):
        for r in self:
            r.existe_fichero = bool(r.fichero and r._buscar_dto())

    rma_id = fields.Many2one(
        comodel_name="repair.order",
        string="RMA de repara",
        ondelete="cascade",
    )
    carpeta = fields.Text(string="Carpeta del fichero", default="/in/Documentacion/RMA")
    fichero = fields.Char(string="Documento")
    existe_fichero = fields.Boolean(
        string="Fichero Encontrado",
        compute="_compute_existe_fichero",
    )
    nota = fields.Text(copy=False)

    def action_ver_docu(self):
        ver_obj = self.env["docu.rma.ver"]
        id_obj1 = ver_obj.search([], limit=1)
        if not id_obj1:
            obj_id = ver_obj.create({})
        else:
            obj_id = id_obj1
        obj_id.write({"docu": self.fichero, "carpeta": self.carpeta})
        return obj_id.ver_docu_rma()

    def _buscar_dto(self):
        if not self.fichero:
            return False
        docu = self.fichero.strip()
        if "." not in docu:
            docu = docu + ".pdf"
        directorio = "/media" + (self.carpeta or "").strip()
        if not os.path.isdir(directorio):
            return False
        for root, _dirs, ficheros in os.walk(directorio):
            for fichero in ficheros:
                if docu == fichero:
                    return os.path.join(root, fichero)
        return False
