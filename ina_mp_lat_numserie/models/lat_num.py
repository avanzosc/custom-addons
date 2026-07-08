# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import shutil
import subprocess

from odoo import fields, models


class LatNum(models.Model):
    _name = "lat.num"
    _description = "Nunmeros serie diario"

    ensayo = fields.Selection(
        [
            ("aisladores", "Aisladores"),
            ("celdas", "Celdas y OCRs"),
            ("centros", "Centros"),
            ("fusibles", "Fusibles"),
            ("pararrayos", "Pararrayos"),
            ("seccionalizadores", "Seccionalizadores"),
            ("selas", "Selas y Seccionadores"),
            ("trafos", "Trafos"),
        ],
    )
    venta_id = fields.Many2one(string="Ord. Venta", comodel_name="sale.order")
    nota = fields.Text()
    lineas_ids = fields.One2many(
        string="Lineas de Numero Serie",
        comodel_name="lat.numserie",
        inverse_name="num_id",
    )

    def action_genera_docus(self):
        # borro el check que tenia, por si lo hago de segunda vez.
        self.lineas_ids.write(
            {
                "decla": False,
                "infens": False,
                "chklis": False,
                "otros": False,
            }
        )
        # Busco Declaraciones
        ruta_origen = "/media/in/Documentacion/Declaracion de conformidad"
        lineas = self.lineas_ids.filtered(
            lambda x: x.product_id and x.product_id.declara_conformi
        )
        for linea in lineas:
            patron = "*" + linea.product_id.declara_conformi.strip() + "*"
            encontrado = self.buscar_dto(ruta_origen, patron)
            if encontrado:
                linea.decla = True

        # Busco Otros
        ruta_origen = "/media/in/Documentacion/Documentacion_protocolos_celdas_centros"
        lineas = self.lineas_ids.filtered(lambda x: x.fichero)
        for linea in lineas:
            patron = "*" + linea.fichero.strip() + "*"
            encontrado = self.buscar_dto(ruta_origen, patron)
            if encontrado:
                linea.otros = True

        # Busco ChkList para Celdas
        ruta_origen = "/media/in/Fabrica/RESULTADOS_ENSAYOS"
        lineas = self.lineas_ids.filtered(lambda x: x.ensayo == "celdas" and x.numserie)
        for linea in lineas:
            encontrado_html = encontrado_doc = False
            patron = "*" + linea.numserie.strip() + "_*.html"
            encontrado_html = self.buscar_dto(ruta_origen, patron)
            if encontrado_html:
                linea.chklis = True
            patron = "*" + linea.numserie.strip() + "_*.docx"
            encontrado_doc = self.buscar_dto(ruta_origen, patron)
            if encontrado_doc:
                linea.chklis = True

        # Imprimo el ensayo de celdas si es ensayo=Celdas
        wizard_informe = self.env["wiz.informe.celdas"]
        lineas = self.lineas_ids.filtered(lambda x: x.ensayo == "celdas" and x.numserie)
        for linea in lineas:
            wiz_ids = wizard_informe.search([("id", ">=", 0)], limit=1)
            if not wiz_ids:
                val = {}
                wiz_ids = wizard_informe.create(val)  # devuelve el id como entero
            wiz_ids.tipo = "celda"
            wiz_ids.generar_pdf(linea.numserie)
            linea.infens = True

    #  --------------- BUSCAR EL DOCUMENTO ---------------------------------
    def buscar_dto(self, ruta_origen, patron):
        ruta_destino = "/media/in/comun/odoo/Calidad/"
        comando = ["find", ruta_origen, "-name", patron]
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE)
        salida, _ = proceso.communicate()
        archivos = salida.decode("utf-8").splitlines()
        for archivo in archivos:
            partes = archivo.split("/")  # Divide la cadena por el separador "/"
            fichero = partes[-1]
            ruta_destino += fichero.strip()
            shutil.copyfile(archivo, ruta_destino)
            return True
        return False
