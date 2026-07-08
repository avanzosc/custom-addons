# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import re

import pytz
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, black, grey
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable

from odoo import _, exceptions, fields, models


class QRFlowable(Flowable):
    # usage :
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


class WizInformeCentro(models.TransientModel):
    _name = "wiz.informe.centro"
    _description = "Informe Centro"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        [("choose", "choose"), ("get", "get")],  # choose language or get the file
        default="choose",
    )

    def _puntuacion(self, cadena):
        reemplazo = {",": ".", ".": ","}
        patron = "|".join(map(re.escape, reemplazo))
        nuevo = re.compile(f"({patron})")
        return nuevo.sub(
            lambda x: reemplazo[x.group(0)],
            cadena,
        )

    def add_to_format(self, existing_format, dict_of_properties, workbook):
        new_dict = {
            key: value
            for key, value in existing_format.__dict__.items()
            if value not in (0, {}) and value is not None
        }
        new_dict.pop("escapes", None)
        new_dict.update(dict_of_properties)
        return workbook.add_format(new_dict)

    def export_pdf(self):
        this = self[0]
        ids = self.env.context["active_ids"]
        if len(ids) < 1:
            raise exceptions.Warning(_("Tienes que seleccionar solamente 1 "))
        self.generar_pdf()
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/centro" + "_" + w_usuario + ".pdf"
        informe_ids = self.env["lat.numcentro"].browse(
            self.env.context.get("active_ids")
        )
        numero_serie = ""
        for cen in informe_ids:
            numero_serie = cen.numserie
        fname = "Informe_centro_" + numero_serie + ".pdf"
        modelo = "wiz.informe.centro"
        fichero_salida = fichero_name
        file_point = open(fichero_salida, "rb")
        file_data = base64.b64encode(file_point.read())
        file_point.close()
        this.write({"state": "get", "data": file_data, "name": fname})
        return {
            "type": "ir.actions.act_window",
            "res_model": modelo,
            "view_mode": "form",
            "view_type": "form",
            "res_id": this.id,
            "views": [(False, "form")],
            "target": "new",
        }

    def generar_pdf(self):
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/centro" + "_" + w_usuario + ".pdf"
        fichero = Canvas(fichero_name)
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        fecha_hoy = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]

        for cen in self.env["lat.numcentro"].browse(self.env.context.get("active_ids")):
            fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
            fichero.setLineWidth(2)
            fichero.roundRect(
                3 * mm, 15 * mm, 204 * mm, 255 * mm, radius=5, stroke=1, fill=0
            )  # si fill=0 no rellena
            fichero.setLineWidth(1)
            fichero.line(3 * mm, 257 * mm, 207 * mm, 257 * mm)
            fichero.line(140 * mm, 270 * mm, 140 * mm, 257 * mm)
            fichero.setFillColor(black)
            fichero.setFillColor(black)
            w_docu = "Informe del Centro " + cen.numserie.strip()
            fichero.setFont("Helvetica-Bold", 14)
            fichero.drawString(5 * mm, 264 * mm, w_docu)
            fichero.setFont("Helvetica", 11)
            fichero.drawString(150 * mm, 262 * mm, fecha_hoy)
            linea = 252
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 10)
            fichero.drawString(5 * mm, linea * mm, "O.F.:")
            fichero.drawString(100 * mm, linea * mm, "O.V.:")
            fichero.setFont("Helvetica-Bold", 10)
            fichero.drawString(15 * mm, linea * mm, cen.production_id.name)
            fichero.drawString(110 * mm, linea * mm, cen.venta_id.name)
            linea -= 5
            fichero.setFont("Helvetica", 8)
            fichero.setFillColor(black)
            fichero.drawString(5 * mm, linea * mm, "Referencia:")
            fichero.setFont("Helvetica-Bold", 10)
            fichero.drawString(20 * mm, linea * mm, cen.default_code)
            fichero.setFont("Helvetica", 8)
            linea -= 5
            fichero.drawString(5 * mm, linea * mm, "Producto:")
            w_pro = cen.product_id.name if cen.product_id else " "
            fichero.drawString(18 * mm, linea * mm, w_pro.strip())
            linea -= 4
            fichero.line(3 * mm, linea * mm, 207 * mm, linea * mm)
            linea = 236
            linea2 = linea - 53
            fichero.setFillColor(HexColor("#FAE9E5"))
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 53 * mm, radius=5, stroke=1, fill=1
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 10)
            fichero.setLineWidth(1)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Inspección Mecanica")
            fichero.drawString(100 * mm, linea * mm, "Inspección Visual  ")
            fichero.setFont("Helvetica", 9)
            linea -= 5
            fichero.drawString(8 * mm, linea * mm, "Instalación Celdas")
            w_c = self.saca_valor(cen.insta_celdas)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Pintura Exterior")
            w_c = self.saca_valor(cen.pintu_exteri)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Montaje de Equipos")
            w_c = self.saca_valor(cen.monta_equipo)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Pintura Interior")
            w_c = self.saca_valor(cen.pintu_interi)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Montaje de Tierras")
            w_c = self.saca_valor(cen.monta_tierra)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Limpieza General")
            w_c = self.saca_valor(cen.limpi_genera)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Caja de Herrajes")
            w_c = self.saca_valor(cen.caja_herraje)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Documentación")
            w_c = self.saca_valor(cen.documentacio)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Montaje de Cerradura")
            w_c = self.saca_valor(cen.monta_cerrad)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Manómetros sf6")
            w_c = self.saca_valor(cen.manom_sf6)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Montaje de Puertas")
            w_c = self.saca_valor(cen.monta_puerta)
            fichero.drawString(71 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Termómetro Trafo")
            w_c = self.saca_valor(cen.termo_trafo)
            fichero.drawString(71 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Sondas Trafo")
            w_c = self.saca_valor(cen.sondas_trafo)
            fichero.drawString(71 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Megado de Tierras")
            w_c = self.saca_valor(cen.mega_tierras)
            fichero.drawString(71 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            linea = 180
            linea2 = linea - 27
            fichero.setFillColor(HexColor("#DAEFF9 "))
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 27 * mm, radius=5, stroke=1, fill=1
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 10)
            fichero.setLineWidth(1)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Accesorios")
            fichero.setFont("Helvetica", 9)
            linea -= 5
            fichero.drawString(8 * mm, linea * mm, "Enclavamientos")
            w_c = self.saca_valor(cen.enclavamien)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Llaves Centro")
            w_c = self.saca_valor(cen.llave_centro)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Palanca Maniobras")
            w_c = self.saca_valor(cen.palan_maniob)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Guantes")
            w_c = self.saca_valor(cen.guantes)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Banqueta")
            w_c = self.saca_valor(cen.banqueta)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Extintor")
            w_c = self.saca_valor(cen.extintor)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Carteleria")
            w_c = self.saca_valor(cen.carteleria)
            fichero.drawString(71 * mm, linea * mm, w_c)
            fichero.drawString(100 * mm, linea * mm, "Alumbrado")
            w_c = self.saca_valor(cen.alumbrado)
            fichero.drawString(163 * mm, linea * mm, w_c)
            linea -= 1
            fichero.line(8 * mm, linea * mm, 70 * mm, linea * mm)
            fichero.line(100 * mm, linea * mm, 162 * mm, linea * mm)
            linea = 150
            linea2 = linea - 20
            fichero.setFillColor(HexColor("#F1F9DC"))
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 20 * mm, radius=5, stroke=1, fill=1
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 12)
            linea -= 5
            fichero.drawString(8 * mm, linea * mm, "Observaciones")
            fichero.setFont("Helvetica", 8)
            fichero.drawString(8 * mm, linea * mm, "")
            fichero.setFont("Helvetica", 8)
            s1 = cen.nota_noblejas
            if s1 is not False:
                cadena = self.listar_notas(s1)
                if len(s1) > 2:
                    linea = linea - 4
                for texto in cadena:
                    if len(texto) > 1:
                        fichero.drawString(8 * mm, linea * mm, texto)
                        linea = linea - 4
            linea = 128
            linea2 = linea - 100
            fichero.setFillColor(black)
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 100 * mm, radius=5, stroke=1, fill=0
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setLineWidth(1)
            linea -= 4
            fichero.setFont("Helvetica-Bold", 12)
            fichero.drawString(8 * mm, linea * mm, "Celdas, Transformadores y Equipos")
            linea -= 6
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawString(8 * mm, linea * mm, "Tipo")
            fichero.drawString(30 * mm, linea * mm, "Número de Serie")
            fichero.drawString(60 * mm, linea * mm, "Producto")
            linea -= 1
            fichero.line(8 * mm, linea * mm, 200 * mm, linea * mm)
            for r in cen.lineas_ids:
                fichero.setFont("Helvetica", 8)
                linea -= 4
                w_t = ""
                if r.ensayo == "celdas":
                    w_t = "Celdas"
                elif r.ensayo == "aisladores":
                    w_t = "Aisladores"
                elif r.ensayo == "edificio":
                    w_t = "Edificio"
                elif r.ensayo == "fusibles":
                    w_t = "Fusibles"
                elif r.ensayo == "pararrayos":
                    w_t = "Pararrayos"
                elif r.ensayo == "seccionalizadores":
                    w_t = "Seccionalizadores"
                elif r.ensayo == "selas":
                    w_t = "Selas/Seccionadores"
                elif r.ensayo == "trafos":
                    w_t = "Trafos"
                elif r.ensayo == "otros":
                    w_t = "Otros"
                fichero.drawString(8 * mm, linea * mm, w_t)
                fichero.drawString(30 * mm, linea * mm, r.numserie)
                fichero.setFont("Helvetica", 7)
                fichero.drawString(60 * mm, linea * mm, r.product_id.name)
            ########## Listo final
            linea = 23
            fichero.setFont("Helvetica-Bold", 11)
            fichero.setFillColor(black)
            wpie1 = fecha_hoy
            fichero.drawString(140 * mm, linea * mm, wpie1)
            linea -= 5
            fichero.drawString(140 * mm, linea * mm, "Calidad")
            fichero.setFillColor(grey)
            fichero.drawString(155 * mm, linea * mm, " / Quality")
            linea -= 2
            logo_cal = ImageReader("/opt/logos/Hoja_Firma_Calidad.png")
            fichero.drawImage(
                logo_cal, 182 * mm, linea * mm, width=62, height=63
            )  # en 580 tenia 600
        fichero.showPage()
        fichero.save()

    def saca_valor(self, w_c1):
        w_c = ""
        if w_c1 == "ok":
            w_c = "Ok"
        elif w_c1 == "nook":
            w_c = "No Ok"
        elif w_c1 == "noap":
            w_c = "No Aplica"
        return w_c

    def listar_notas(self, s1):
        s1 = s1 + "\n"
        s2 = s1.split("\n")
        cadena = []
        for sc in s2:
            c = []
            if len(sc) > 142:
                c = sc.split()
                c2 = ""
                for c1 in c:
                    c2 += c1 + " "
                    if len(c2) >= 142:
                        cadena.append(c2)
                        c2 = ""
                cadena.append(c2)
            else:
                cadena.append(sc)
        cadena.append(c)
        return cadena
