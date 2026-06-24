# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Para ejecutar comandos del sistema
import base64
import os

# Para poner puntuacion decimal, necesitamos re para reeemplazar
import re
import shlex
import subprocess
from io import BytesIO

# import xmlrpclib
# from PyPDF2 import PdfFileMerger
import pytz
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, black, lightgrey, red
from reportlab.lib.units import mm

# Para hacer PDF
# y tambien para Codigo de Barras
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable

from odoo import _, fields, models
from odoo.exceptions import UserError


class QRFlowable(Flowable):
    # usage:
    # story.append(QRFlowable("http://google.fr"))
    def __init__(self, qr_value):
        # init and store rendering value
        Flowable.__init__(self)
        self.qr_value = qr_value

    def wrap(self, availWidth, availHeight):
        # optionnal, here I ask for the biggest square available
        self.width = self.height = min(availWidth, availHeight)
        self.width = 60
        self.height = 60
        return self.width, self.height

    def draw(self):
        # here standard and documented QrCodeWidget usage on
        # Flowable canva
        qr_code = qr.QrCodeWidget(self.qr_value)
        bounds = qr_code.getBounds()
        qr_width = bounds[2] - bounds[0]
        qr_height = bounds[3] - bounds[1]
        w = float(self.width)
        d = Drawing(w, w, transform=[w / qr_width, 0, 0, w / qr_height, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, self.canv, 0, 0)


class ListarOlaser(models.TransientModel):
    _name = "wiz.listar.olaser"
    _description = "Listar OLaser"

    name = fields.Char("File Name", readonly=True)
    data = fields.Binary("File", readonly=True)

    def _puntuacion(self, cadena):
        reemplazo = {",": ".", ".": ","}
        pattern = "|".join(map(re.escape, reemplazo.keys()))
        nuevo = re.compile(rf"({pattern})")
        return nuevo.sub(lambda x: reemplazo[x.group(0)], cadena)

    def add_to_format(self, existing_format, dict_of_properties, workbook):
        """Give a format you want to extend and a dict of the properties you want to
        extend it with, and you get them returned in a single format"""
        new_dict = {}
        for key, value in existing_format.__dict__.iteritems():
            if (value != 0) and (value != {}) and (value is not None):
                new_dict[key] = value
        del new_dict["escapes"]
        return workbook.add_format(dict(new_dict.items() + dict_of_properties.items()))

    def export_pdf(self):
        buffer_of = self.listar_olaser()
        #  * NECESITA CONTROLLER ******** PARA PERMITIR LA DESCARGA DIRECTA
        pdf_bytes = buffer_of.getvalue()
        pdf_b64 = base64.b64encode(pdf_bytes)
        self.env["ir.config_parameter"].sudo().set_param(
            f"ver_pdf_{self.env.uid}", pdf_b64.decode()
        )
        fname = "olaser.pdf"
        return {
            "type": "ir.actions.act_url",
            "url": f"/my/direct/download_pdf?fname={fname}",
            "target": "self",
        }

    def listar_olaser(self):
        #  memoria en lugar de fichero en disco
        buffer_of = BytesIO()
        fichero = Canvas(buffer_of)
        #  Estos de Hoja
        #  fichero.drawImage(logo,2*mm, 285*mm, width=80 , height=23, mask="auto")
        #  en 580 tenia 600
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        fecha_hoy = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
        hora_hoy = fec[11:19]
        for of in self.env["order.olaser"].browse(self.env.context.get("active_ids")):
            w_of = of.name
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 12)
            fichero.drawString(4 * mm, 285 * mm, "INAEL")
            fichero.drawString(40 * mm, 285 * mm, "Orden: ")
            fichero.drawString(54 * mm, 285 * mm, w_of)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(180 * mm, 285 * mm, fecha_hoy + "  " + hora_hoy)
            fichero.setFillColor(red)
            fichero.setFont("Helvetica", 12)
            fichero.drawString(123 * mm, 285 * mm, "ID:")
            fichero.setFont("Helvetica-Bold", 16)
            sid = self._puntuacion(str(f"{of.id:,.0f}"))
            fichero.drawString(130 * mm, 285 * mm, "L" + sid)
            fichero.setFillColor(black)
            fichero.line(1 * mm, 284 * mm, 208 * mm, 284 * mm)
            linea = 277
            fichero.setFont("Helvetica", 8)
            fichero.drawString(5 * mm, linea * mm, "Materia Prima:")
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawString(
                25 * mm,
                linea * mm,
                of.product_id.default_code.strip() + " - " + of.product_id.name.strip(),
            )
            linea -= 7
            fichero.setFont("Helvetica", 8)
            fichero.drawString(5 * mm, linea * mm, "Cantidad:")
            fichero.setFont("Helvetica-Bold", 8)
            scantidad = self._puntuacion(str(f"{of.cantidad:,.2f}"))
            fichero.drawString(20 * mm, linea * mm, scantidad)
            linea -= 7
            fichero.setFont("Helvetica", 8)
            fichero.drawString(5 * mm, linea * mm, "Peso Kgs:")
            fichero.setFont("Helvetica-Bold", 8)
            scantidad = self._puntuacion(str(f"{of.peso_mp:,.2f}"))
            fichero.drawString(20 * mm, linea * mm, scantidad)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(65 * mm, linea * mm, "Tiempo Total (min):")
            fichero.setFont("Helvetica-Bold", 8)
            scantidad = self._puntuacion(str(f"{of.tiempo_total:,.0f}"))
            fichero.drawString(90 * mm, linea * mm, scantidad)
            linea -= 10
            fichero.setFillColor(red)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(5 * mm, linea * mm, "Referencia")
            fichero.drawString(35 * mm, linea * mm, "Descripcion")
            fichero.drawString(130 * mm, linea * mm, "Qt.Chapa")
            fichero.drawString(145 * mm, linea * mm, "Plano Actual")
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(3 * mm, linea * mm, 160 * mm, linea * mm)
            fichero.line(33 * mm, linea * mm, 33 * mm, (linea + 5) * mm)
            fichero.line(127 * mm, linea * mm, 127 * mm, (linea + 5) * mm)
            fichero.line(143 * mm, linea * mm, 143 * mm, (linea + 5) * mm)
            fichero.setStrokeColor(black)
            for oz in of.listas_ids:
                linea -= 4
                w_cantidad = oz.cantidad_chapa
                if w_cantidad is None:
                    w_cantidad = 0
                scantidad = self._puntuacion(str(f"{w_cantidad:,.2f}"))
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 7)
                fichero.drawString(5 * mm, linea * mm, oz.product_id.default_code)
                fichero.setFont("Helvetica", 7)
                fichero.drawString(35 * mm, linea * mm, oz.product_id.name[:35])
                fichero.setFont("Helvetica-Bold", 8)
                #  if oz.product_id.plano:  # anulo para que no salga el plano
                #      self.copiar_plano(oz.product_id.plano)
                fichero.drawRightString(138 * mm, linea * mm, scantidad)
                fichero.setFont("Helvetica-Bold", 7)
                fichero.drawString(145 * mm, linea * mm, oz.product_id.plano.strip())
                fichero.setFont("Helvetica", 8)
                sql = """
                    SELECT id, plano
                    FROM order_olaser_lista
                    WHERE id < %s
                      AND product_id = %s
                    ORDER BY id DESC
                    LIMIT 1
                """
                self.env.cr.execute(sql, (oz.id, oz.product_id.id))
                res = self.env.cr.dictfetchall()
                w_plano = False
                w_primera = True
                for r in res:
                    w_primera = False
                    w_pla = r["plano"]
                    if oz.plano != w_pla:
                        w_plano = True
                if w_primera:
                    fichero.setFillColor(HexColor("#FAE9E5"))
                    fichero.roundRect(
                        180 * mm,
                        linea * mm,
                        190 * mm,
                        4 * mm,
                        radius=5,
                        stroke=0,
                        fill=1,
                    )  # si fill=0 no rellena
                    fichero.setFillColor(black)
                    fichero.setFillColor(red)
                    fichero.setFont("Helvetica-Bold", 6)
                    fichero.drawString(
                        185 * mm, (linea + 1) * mm, "Atencion: Primera fabricación"
                    )
                elif w_plano:
                    fichero.setFillColor(HexColor("#FAE9E5"))
                    fichero.roundRect(
                        180 * mm,
                        linea * mm,
                        190 * mm,
                        4 * mm,
                        radius=5,
                        stroke=0,
                        fill=1,
                    )  # si fill=0 no rellena
                    fichero.setFillColor(black)
                    fichero.setFillColor(red)
                    fichero.setFont("Helvetica-Bold", 6)
                    fichero.drawString(
                        185 * mm, (linea + 1) * mm, "Atencion: Cambio de Plano"
                    )
                if oz.product_id.inspeccion_of:
                    fichero.setFillColor(red)
                    fichero.setFont("Helvetica-Bold", 7)
                    fichero.drawString(
                        160 * mm, linea * mm, "Ref. Critica. Inspeccionar"
                    )
                    fichero.setFillColor(black)
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(3 * mm, linea * mm, 160 * mm, linea * mm)
                fichero.line(33 * mm, linea * mm, 33 * mm, (linea + 5) * mm)
                fichero.line(127 * mm, linea * mm, 127 * mm, (linea + 5) * mm)
                fichero.line(143 * mm, linea * mm, 143 * mm, (linea + 5) * mm)
                fichero.setStrokeColor(black)
                if linea <= 30:
                    self.cabecera_olaser(fichero, w_of, fecha_hoy, hora_hoy)
                    linea = 270
        # salto de pagina
        fichero.showPage()
        fichero.save()
        #  MUY IMPORTANTE: rebobinar buffer
        buffer_of.seek(0)
        return buffer_of

    def listar_notas(self, s1):
        if not s1:
            s1 = " "
        s1 = s1 + "\n"
        s2 = s1.split("\n")
        cadena = []
        for sc in s2:
            c = []
            if len(sc) > 150:
                c = sc.split()
                c2 = ""
                for c1 in c:
                    c2 += c1 + " "
                    if len(c2) >= 150:
                        cadena.append(c2)
                        c2 = ""
                cadena.append(c2)
            else:
                cadena.append(sc)
        cadena.append(c)
        return cadena

    def cabecera_olaser(self, fichero, w_of, fecha_hoy, hora_hoy):
        linea = 280
        fichero.showPage()
        fichero.setFillColor(red)
        fichero.setFont("Helvetica", 8)
        fichero.drawString(5 * mm, linea * mm, "Referencia")
        fichero.drawString(35 * mm, linea * mm, "Descripcion")
        fichero.drawString(130 * mm, linea * mm, "Qt.Chapa")
        linea -= 1
        fichero.setStrokeColor(lightgrey)
        fichero.line(3 * mm, linea * mm, 147 * mm, linea * mm)
        fichero.line(33 * mm, linea * mm, 33 * mm, (linea + 5) * mm)
        fichero.line(127 * mm, linea * mm, 127 * mm, (linea + 5) * mm)
        fichero.setStrokeColor(black)

    def copiar_plano(self, w_plano):
        w_dir = "/media/in/Documentacion/Planos de Proveedor"
        fichero_name = self.buscar_dto(w_dir, w_plano)

        if not fichero_name:
            w_dir = "/media/in/Documentacion/Planos de Clientes"
            fichero_name = self.buscar_dto(w_dir, w_plano)
        if not fichero_name:
            return  # NO Encontrado, vuelvo
        w_file = fichero_name
        w_usuario = (self.env.user.login).strip()
        destino = "/media/in/Comun/odoo/fabrica/"
        if w_usuario == "macorrales":
            destino = "/media/in/Comun/odoo/fabrica/" + "macorrales/"
        if w_usuario == "rcadarso":
            destino = "/media/in/Comun/odoo/fabrica/" + "rcadarso/"
        elif w_usuario == "jpeces":
            destino = "/media/in/Comun/odoo/fabrica/" + "jpeces/"
        elif w_usuario == "adlara":
            destino = "/media/in/Comun/odoo/fabrica/" + "adlara/"
        elif w_usuario == "jvernandez":
            destino = "/media/in/Comun/odoo/fabrica/" + "jfernandez/"
        elif w_usuario == "admin":
            destino = "/media/in/Comun/odoo/fabrica/" + "admin/"
        #  Ejecuto el comando de copia si existe
        if os.path.exists(w_file):
            comando = "cp  " " +(w_file) + " " " + destino
            coman1 = comando.encode("utf-8")
            #  comando=coman1.decode("utf-8")
            comando = coman1
            arg = shlex.split(comando)
            subprocess.call(arg)

    def buscar_dto(self, directorio, plano):
        #  directorio = os.getcwd()
        plano = plano.strip()
        if not os.path.isdir(directorio):
            raise UserError(_("El directorio no existe."))
        for root, _directo, ficheros in os.walk(directorio):
            for fichero in ficheros:
                # if(buscar in fichero.lower()):
                fichero = fichero.decode("utf-8")
                if plano in fichero:
                    #  self.ruta = root[23:]+"/"+fichero
                    #  w_d = root.lower() #Traduzco dir a minusculas
                    #  w_x = w_d.find("anulad")  # busco la cadena anulad
                    #  if w_x >= 0:  # es porque fue encontrado en anulado
                    #     self.anulado = True
                    return root + "/" + fichero
        return False
