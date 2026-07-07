# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Para ejecutar comandos del sistema
import base64

# Para poner puntuacion decimal, necesitamos re para reeemplazar
import re
import shutil

import pytz
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, black, grey, lightgrey, red
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

# Para hacer PDF
# y tambien para Codigo de Barras
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


class WizInformeCeldas(models.TransientModel):
    _name = "wiz.informe.celdas"
    _description = "Listar Informe Celdas"

    name = fields.Char("File Name", readonly=True)
    data = fields.Binary("File", readonly=True)
    state = fields.Selection(
        [("choose", "choose"), ("get", "get")],  # choose language or get the file
        default="choose",
    )
    tipo = fields.Selection(
        [("celda", "Celda"), ("gnf", "OCR GNF")],
        string="Tipo de Informe",
        default="celda",
    )

    def _puntuacion(self, cadena):
        reemplazo = {",": ".", ".": ","}
        nuevo = re.compile(f"({'|'.join(map(re.escape, reemplazo.keys()))})")
        return nuevo.sub(
            lambda x: str(reemplazo[x.string[x.start() : x.end()]]), cadena
        )

    def add_to_format(self, existing_format, dict_of_properties, workbook):
        new_dict = {}
        for key, value in existing_format.__dict__.items():
            if value != 0 and value != {} and value is not None:
                new_dict[key] = value
        new_dict.pop("escapes", None)
        return workbook.add_format(dict(new_dict.items() + dict_of_properties.items()))

    def export_pdf(self):
        this = self[0]
        ids = self.env.context["active_ids"]
        if len(ids) < 1:
            raise exceptions.Warning(_("Tienes que seleccionar solamente 1"))
        self.generar_pdf(False)
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/celda" + "_" + w_usuario + ".pdf"
        informe_ids = self.env["res.celdas"].browse(self.env.context.get("active_ids"))
        numero_serie = "x"
        for cel in informe_ids:
            w_n = cel.celda_num if cel.celda_num else 0
            numero_serie = self._puntuacion(str(f"{w_n:,.0f}"))
        if self.tipo == "celda":
            fname = "Informe_celda_" + numero_serie + ".pdf"
        elif self.tipo == "gnf":
            fname = "Informe_celda_gnf_" + numero_serie + ".pdf"
        modelo = "wiz.informe.celdas"
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

    def generar_pdf(self, w_celda_numero):
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/celda" + "_" + w_usuario + ".pdf"
        #       fichero= (fichero_name)
        fichero = Canvas(fichero_name)
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        fecha_hoy = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
        if w_celda_numero:
            informe_ids = self.env["res.celdas"].search(
                [("celda_num", "=", w_celda_numero)]
            )
        else:
            informe_ids = self.env["res.celdas"].browse(
                self.env.context.get("active_ids")
            )
        for cel in informe_ids:
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", cel.product_id.id), ("ensayo_id", "=", 66)]
            )  # 66 es Nota de Pie Informe
            if ens_ids:
                if not ens_ids.nota:
                    ens_ids.nota = " "
                w_nota_pie = ens_ids.nota.strip()
            else:
                w_nota_pie = False

            fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
            fichero.setLineWidth(2)
            #           fichero.rect(3*mm,15*mm,204*mm,255*mm)
            fichero.roundRect(
                3 * mm, 15 * mm, 204 * mm, 255 * mm, radius=5, stroke=1, fill=0
            )  # si fill=0 no rellena
            fichero.setLineWidth(1)
            fichero.setFillColor(black)
            linea = 264
            w_n = cel.celda_num if cel.celda_num else 0
            numero_serie = self._puntuacion(str(f"{w_n:,.0f}"))
            #           fichero.drawRightString(110*mm,linea*mm, shoras )
            w_docu = (
                "Protocolo de Celdas e Interruptores M.T. de SF6 "
                + "    Nº "
                + numero_serie.strip()
            )
            fichero.setFont("Helvetica-Bold", 14)
            fichero.drawString(5 * mm, linea * mm, w_docu)
            fichero.setFont("Helvetica", 11)
            fec = str(cel.celda_fecha)
            wfecha = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
            fichero.drawString(165 * mm, linea * mm, wfecha)
            linea -= 7
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 10)
            fichero.drawString(5 * mm, linea * mm, cel.product_id.default_code)
            fichero.setFont("Helvetica", 8)
            w_n = cel.product_id.name if cel.product_id.name else " "
            fichero.drawString(50 * mm, linea * mm, w_n[:60])
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", cel.product_id.id), ("ensayo_id", "=", 18)]
            )  # 18 es la norma aplicable
            if ens_ids:
                w_norma = ens_ids.etiqueta.strip()
            else:
                w_norma = False
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", cel.product_id.id), ("ensayo_id", "=", 65)]
            )  # 18 es la norma aplicable
            if ens_ids:
                w_norma2 = ens_ids.etiqueta.strip()
            else:
                w_norma2 = False
            linea -= 5
            if w_norma:
                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.drawString(5 * mm, linea * mm, "Fabricado segun normas")
                fichero.setFillColor(grey)
                fichero.drawString(37 * mm, linea * mm, "/ Manufacured according to:")
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawString(74 * mm, linea * mm, w_norma)
            if w_norma2:
                linea -= 4
                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawString(74 * mm, linea * mm, w_norma2)
                linea += 4
            ########## Listo Llenado
            linea -= 10
            linea2 = linea - 22
            #           fichero.setFillColor(HexColor("#FBE2DD") )
            fichero.setFillColor(HexColor("#FAE9E5"))
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 22 * mm, radius=5, stroke=1, fill=1
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 12)
            linea -= 4
            fichero.drawString(8 * mm, linea * mm, "Llenado de Gas")
            fichero.setFont("Helvetica-Bold", 10)
            fichero.drawString(40 * mm, linea * mm, "/ Gas Filling")
            linea -= 7
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(8 * mm, linea * mm, "Nivel de Fuga")
            fichero.setFillColor(grey)
            fichero.drawString(26 * mm, linea * mm, "/ Leakage level:")
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 8)
            w_n = cel.niv_fuga_med if cel.niv_fuga_med else 0
            s_n = format(w_n, ".2E")
            fichero.drawRightString(177 * mm, linea * mm, s_n)
            fichero.drawString(178 * mm, linea * mm, " mbar l/seg")
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
            fichero.setStrokeColor(black)
            linea -= 5
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(8 * mm, linea * mm, "Presión final de llenado")
            fichero.setFillColor(grey)
            fichero.drawString(38 * mm, linea * mm, "/ Final pressure of filling:")
            fichero.setFillColor(black)
            w_n = cel.niv_llen_med if cel.niv_llen_med else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawRightString(177 * mm, linea * mm, s_n)
            fichero.drawString(178 * mm, linea * mm, " mbar abs")
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
            fichero.setStrokeColor(black)
            ########## Listo Ensayo Dielectrico
            linea -= 10
            if self.tipo == "celda":
                linea2 = linea - 50
                fichero.setFillColor(HexColor("#F1F9DC"))
                fichero.roundRect(
                    5 * mm, linea2 * mm, 200 * mm, 50 * mm, radius=5, stroke=1, fill=1
                )  # si fill=0 no rellena
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 12)
                linea -= 4
                fichero.drawString(8 * mm, linea * mm, "Ensayo Dielectrico")
                fichero.setFont("Helvetica-Bold", 10)
                fichero.drawString(48 * mm, linea * mm, "/ Dielectric Tests")
                fichero.setFont("Helvetica", 8)
                linea -= 5
                fichero.setFillColor(black)
                fichero.drawString(
                    8 * mm,
                    linea * mm,
                    "Tensión soportada a frecuencia Industrial del circuito principal",
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    86 * mm,
                    linea * mm,
                    "/ Power frecuency dielectric tests over the main circuit:",
                )
                fichero.setFillColor(black)
                w_n = cel.v_ens_tierra if cel.v_ens_tierra else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm,
                    linea * mm,
                    (
                        "Tensión soportada a frecuencia Industrial de "
                        "los circuitos auxiliares "
                    ),
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    93 * mm,
                    linea * mm,
                    (
                        "/ Power frequency dielectric tests "
                        "over the auxiliary circuit:"
                    ),
                )
                fichero.setFillColor(black)
                w_n = cel.v_ens_circu if cel.v_ens_circu else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm,
                    linea * mm,
                    (
                        "Tensión soportada a frecuencia Industrial de "
                        "la bobina de disparo"
                    ),
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    91 * mm,
                    linea * mm,
                    ("/ Power frequency dielectric tests " "over the trip coil:"),
                )
                fichero.setFillColor(black)
                w_n = cel.v_ens_bobina if cel.v_ens_bobina else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm, linea * mm, "Tensión de disparo máximo de la bobina "
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    61 * mm, linea * mm, "/ Maximun voltage for tripping coil:"
                )
                fichero.setFillColor(black)
                w_n = cel.v_supe_disparo1 if cel.v_supe_disparo1 else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " V")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm, linea * mm, "Tensión de disparo mínima de la bobina "
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    61 * mm, linea * mm, "/ Minimun voltage for tripping coil:"
                )
                fichero.setFillColor(black)
                w_n = cel.v_infe_disparo1 if cel.v_infe_disparo1 else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " V")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(8 * mm, linea * mm, "Tiempo de disparo medido ")
                fichero.setFillColor(grey)
                fichero.drawString(43 * mm, linea * mm, "/ Operation time measure:")
                fichero.setFillColor(black)
                w_n = cel.tiempo_dis_medido if cel.tiempo_dis_medido else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " ms")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm, linea * mm, "Funcionamiento de la presencia de tensión "
                )
                fichero.setFillColor(grey)
                fichero.drawString(64 * mm, linea * mm, "/ Voltage boxes:")
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, "OK")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
            elif self.tipo == "gnf":
                linea2 = linea - 45
                fichero.setFillColor(HexColor("#F1F9DC"))
                fichero.roundRect(
                    5 * mm, linea2 * mm, 200 * mm, 45 * mm, radius=5, stroke=1, fill=1
                )  # si fill=0 no rellena
                fichero.setFillColor(black)
                fichero.setFont("Helvetica-Bold", 12)
                linea -= 4
                fichero.drawString(8 * mm, linea * mm, "Ensayo Dielectrico")
                fichero.setFont("Helvetica-Bold", 10)
                fichero.drawString(48 * mm, linea * mm, "/ Dielectric Tests")
                fichero.setFont("Helvetica", 8)
                linea -= 5
                fichero.setFillColor(black)
                fichero.drawString(
                    8 * mm,
                    linea * mm,
                    "Tensión soportada a frecuencia Industrial del circuito principal",
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    86 * mm,
                    linea * mm,
                    "/ Power frecuency dielectric tests over the main circuit",
                )
                fichero.setFillColor(black)
                linea -= 5
                w_n = cel.v_ens_tierra if cel.v_ens_tierra else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.drawString(
                    12 * mm,
                    linea * mm,
                    (
                        "-POSICIÓN 1: Interruptor ABIERTO, Tensión en 'ABC' "
                        "y Tierra en 'abc' y carcasa:"
                    ),
                )
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.drawString(
                    12 * mm,
                    linea * mm,
                    (
                        "-POSICIÓN 2: Interruptor ABIERTO, Tensión en 'abc' "
                        "y Tierra en 'ABC' y carcasa:"
                    ),
                )
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5

                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.drawString(
                    12 * mm,
                    linea * mm,
                    (
                        "-POSICIÓN 3: Interruptor CERRADO, Tensión en 'AaCc' "
                        "y Tierra en 'Bb' y carcasa:"
                    ),
                )
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5
                fichero.setFont("Helvetica", 8)
                fichero.setFillColor(black)
                fichero.drawString(
                    12 * mm,
                    linea * mm,
                    (
                        "-POSICIÓN 4: Interruptor CERRADO, Tensión en 'Bb' "
                        "y Tierra en 'AaCc' y carcasa:"
                    ),
                )
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
                linea -= 5

                fichero.setFillColor(black)
                fichero.setFont("Helvetica", 8)
                fichero.drawString(
                    8 * mm,
                    linea * mm,
                    (
                        "Tensión soportada a frecuencia Industrial "
                        "de los circuitos auxiliares"
                    ),
                )
                fichero.setFillColor(grey)
                fichero.drawString(
                    93 * mm,
                    linea * mm,
                    "/ Power frecuency dielectric tests over the auxliary circuit:",
                )
                fichero.setFillColor(black)
                w_n = cel.v_ens_circu if cel.v_ens_circu else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.setFont("Helvetica-Bold", 8)
                fichero.drawRightString(177 * mm, linea * mm, s_n)
                fichero.drawString(178 * mm, linea * mm, " kV/1 min")
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
                fichero.setStrokeColor(black)
            ########## Listo Embolsamiento
            linea -= 10
            linea2 = linea - 20
            fichero.setFillColor(HexColor("#D8EBFF"))
            fichero.roundRect(
                5 * mm, linea2 * mm, 200 * mm, 20 * mm, radius=5, stroke=1, fill=1
            )  # si fill=0 no rellena
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 12)
            linea -= 4
            fichero.drawString(
                8 * mm, linea * mm, "Embolsamiento y Controles Generales "
            )
            fichero.setFont("Helvetica-Bold", 10)
            fichero.drawString(
                87 * mm, linea * mm, "/ Gas-Pocket test and general controls"
            )
            fichero.setFont("Helvetica", 8)
            linea -= 7
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(
                8 * mm, linea * mm, "Enclavamientos y maniobras de apertura y cierre "
            )
            fichero.setFillColor(grey)
            fichero.drawString(
                70 * mm, linea * mm, "/ Locks and operating cicles (open and close):"
            )
            fichero.setFillColor(black)
            w_n = cel.tiempo_dis_medido if cel.tiempo_dis_medido else 0
            s_n = "OK" if cel.enclavamientos else ""
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawRightString(177 * mm, linea * mm, "OK")
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
            fichero.setStrokeColor(black)
            linea -= 5
            fichero.setFillColor(black)
            fichero.setFont("Helvetica", 8)
            fichero.drawString(8 * mm, linea * mm, "Señalizaciones visuales  ")
            fichero.setFillColor(grey)
            fichero.drawString(40 * mm, linea * mm, "/ Visual signaling: ")
            fichero.setFillColor(black)
            s_n = "OK" if cel.inspec_visual else ""
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawRightString(177 * mm, linea * mm, "OK")
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(8 * mm, linea * mm, 198 * mm, linea * mm)
            fichero.setStrokeColor(black)
            ########## Listo Seccionadores
            linea -= 15
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 12)
            linea -= 4
            fichero.drawString(
                8 * mm, linea * mm, "Resistencia Circuito y tiempos de maniobra "
            )
            fichero.setFont("Helvetica-Bold", 11)
            fichero.drawString(
                100 * mm, linea * mm, "/ Circuit resistance and operation times"
            )
            linea -= 7
            fichero.setFont("Helvetica-Bold", 8)
            fichero.setFillColor(red)
            fichero.drawString(8 * mm, linea * mm, "Seccionadores")
            fichero.drawString(35 * mm, linea * mm, "Denominación")
            fichero.drawString(92 * mm, linea * mm, "R")
            fichero.drawString(107 * mm, linea * mm, "S")
            fichero.drawString(123 * mm, linea * mm, "T")
            fichero.setFillColor(red)
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawString(140 * mm, linea * mm, "Apertura")
            fichero.setFillColor(grey)
            fichero.setFont("Helvetica-Bold", 7)
            fichero.drawString(153 * mm, linea * mm, "/ Opening")
            fichero.setFillColor(red)
            fichero.setFont("Helvetica-Bold", 8)
            fichero.drawString(175 * mm, linea * mm, "Cierre")
            fichero.setFillColor(grey)
            fichero.setFont("Helvetica-Bold", 7)
            fichero.drawString(184 * mm, linea * mm, "/ Closing")
            linea -= 3
            fichero.setFillColor(red)
            fichero.setFont("Helvetica-Bold", 8)
            w_ohm = "(" + "\u00b5" + "\u2126" + ")"
            fichero.drawString(91 * mm, linea * mm, w_ohm)
            fichero.drawString(106 * mm, linea * mm, w_ohm)
            fichero.drawString(121 * mm, linea * mm, w_ohm)
            fichero.drawString(150 * mm, linea * mm, "(ms)")
            fichero.drawString(180 * mm, linea * mm, "(ms)")
            fichero.setFillColor(black)
            fichero.setLineWidth(1)
            linea -= 1
            fichero.line(7 * mm, linea * mm, 200 * mm, linea * mm)
            for t in cel.lineas_ids:
                linea -= 4
                fichero.setFont("Helvetica", 8)
                fichero.drawString(8 * mm, linea * mm, t.seccionador)
                fichero.setFont("Helvetica", 7)
                fichero.drawString(35 * mm, linea * mm, t.descripcion)
                fichero.setFont("Helvetica", 8)
                w_n = t.res_r_med if t.res_r_med else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(97 * mm, linea * mm, s_n)
                w_n = t.res_s_med if t.res_s_med else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(113 * mm, linea * mm, s_n)
                w_n = t.res_t_med if t.res_t_med else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(129 * mm, linea * mm, s_n)
                w_n = t.vel_aper_med if t.vel_aper_med else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(156 * mm, linea * mm, s_n)
                w_n = t.vel_cier_med if t.vel_cier_med else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(186 * mm, linea * mm, s_n)
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(8 * mm, linea * mm, 200 * mm, linea * mm)
                fichero.line(34 * mm, linea * mm, 34 * mm, (linea + 5) * mm)
                fichero.line(85 * mm, linea * mm, 85 * mm, (linea + 5) * mm)
                fichero.line(99 * mm, linea * mm, 99 * mm, (linea + 5) * mm)
                fichero.line(115 * mm, linea * mm, 115 * mm, (linea + 5) * mm)
                fichero.line(131 * mm, linea * mm, 131 * mm, (linea + 5) * mm)
                fichero.line(168 * mm, linea * mm, 168 * mm, (linea + 5) * mm)
                fichero.setStrokeColor(black)
            ########## Listo final
            linea = 25
            tz = pytz.timezone("Europe/Madrid")
            fec0 = fields.datetime.now(tz)
            fec = str(fec0)
            fecha_hoy = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
            if w_nota_pie:
                fichero.setFont("Helvetica", 7)
                fichero.setFillColor(black)
                fichero.drawString(6 * mm, linea * mm, w_nota_pie)
            fichero.setFont("Helvetica-Bold", 12)
            fichero.setFillColor(black)
            wpie1 = fecha_hoy
            fichero.drawString(140 * mm, linea * mm, wpie1)
            linea -= 5
            fichero.drawString(140 * mm, linea * mm, "Calidad")
            fichero.setFillColor(grey)
            fichero.drawString(160 * mm, linea * mm, " / Quality")
            logo_cal = ImageReader("/opt/logos/Hoja_Firma_Calidad.png")
            fichero.drawImage(
                logo_cal, 182 * mm, linea * mm, width=62, height=63
            )  # en 580 tenia 600
        fichero.showPage()
        fichero.save()
        if w_celda_numero:
            # copio a comun/Calidad porque viene w_celda_numero que lo envia
            # el modulo de numeros de serie
            w_fichero = numero_serie.strip()
            ruta_destino = "/media/in/Comun/odoo/Calidad/Informe_" + w_fichero + ".pdf"
            shutil.copyfile(fichero_name, ruta_destino)
