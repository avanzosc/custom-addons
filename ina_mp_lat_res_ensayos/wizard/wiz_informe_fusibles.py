# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64

# Para poner puntuacion decimal, necesitamos re para reeemplazar
import re

# import xmlrpclib
import pytz
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import black, grey, lightgrey, red
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

# Para hacer PDF
# y tambien para Codigo de Barras
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable

from odoo import _, api, exceptions, fields, models


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


class WizInformeFusibles(models.TransientModel):
    _name = "wiz.informe.fusibles"
    _description = "Listar Informe Fusibles"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        [("choose", "choose"), ("get", "get")],  # choose language or get the file
        default="choose",
    )
    pedido_cliente = fields.Char()
    listar_rechazos = fields.Boolean(default=False)

    @api.model
    def _dirty_check(self):
        ids = self.env.context["active_ids"]
        if len(ids) < 1:
            raise exceptions.Warning(_("Tienes que seleccionar al menos 1 Fusible"))

        return {}

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        """Changes the view dynamically
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param context: A standard dictionary
        @return: New arch of view.
        """
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False
        )
        self._dirty_check()
        return res

    def _puntuacion(self, cadena):
        reemplazo = {",": ".", ".": ","}
        nuevo = re.compile(f"({'|'.join(map(re.escape, reemplazo.keys()))})")
        return nuevo.sub(
            lambda x: reemplazo[x.group(0)],
            cadena,
        )

    def add_to_format(self, existing_format, dict_of_properties, workbook):
        """Give a format you want to extend and a dict of the properties you want to
        extend it with, and you get them returned in a single format."""
        new_dict = {}
        for key, value in existing_format.__dict__.items():
            if value != 0 and value != {} and value is not None:
                new_dict[key] = value

        new_dict.pop("escapes", None)
        return workbook.add_format(dict(new_dict.items() + dict_of_properties.items()))

    def export_pdf(self):
        prime = True
        produc = False
        for r in self.env["res.fusibles"].browse(self.env.context.get("active_ids")):
            if prime:
                prime = False
                produc = r.product_id.id
            if produc != r.product_id.id:
                raise exceptions.Warning(
                    _(
                        "Los fusibles seleccionados tienen que tener "
                        "la misma referencia."
                    )
                )
        this = self[0]
        self.generar_pdf()
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/fusibles" + "_" + w_usuario + ".pdf"
        fname = "fusibles.pdf"
        modelo = "wiz.informe.fusibles"
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
        fichero_name = "/tmp/fusibles" + "_" + w_usuario + ".pdf"
        #       fichero= (fichero_name)
        fichero = Canvas(fichero_name)
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        w_pagina = 0
        fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
        fichero.setLineWidth(2)
        #       fichero.rect(3*mm,15*mm,204*mm,255*mm)
        fichero.roundRect(
            2 * mm, 15 * mm, 205 * mm, 255 * mm, radius=5, stroke=1, fill=0
        )  # si fill=0 no rellena
        fichero.setLineWidth(1)
        fichero.setFont("Helvetica", 6)
        w_pagina += 1
        fichero.drawString(195 * mm, 285 * mm, "Pag. " + str(w_pagina))
        fichero.setFillColor(black)
        linea = 264
        fichero.setFillColor(black)
        fichero.setFont("Helvetica-Bold", 12)
        fichero.drawString(6 * mm, linea * mm, "Informe de ensayos - Fusibles ")
        fichero.setFont("Helvetica-Bold", 11)
        fichero.drawString(
            75 * mm, linea * mm, "  Test report - Current limiting fuses  "
        )
        linea = 257
        fichero.setFont("Helvetica", 9)
        fichero.setFillColor(black)
        fichero.drawString(6 * mm, linea * mm, "Referencia Cliente")
        fichero.setFillColor(grey)
        fichero.drawString(32 * mm, linea * mm, " / Customer reference:")
        fichero.setFillColor(black)
        fichero.drawString(100 * mm, linea * mm, "Tipo de Fusible ")
        fichero.setFillColor(grey)
        fichero.drawString(122 * mm, linea * mm, " / Fuse type: ")
        fichero.setFillColor(black)
        linea = 252
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(9 * mm, linea * mm, 204 * mm, linea * mm)
        linea = 249
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(10 * mm, linea * mm, "Num. Serie")
        #       fichero.drawString(25*mm,linea*mm, "Referencia")
        fichero.drawString(40 * mm, linea * mm, "Resistencia Nominal")
        fichero.drawString(77 * mm, linea * mm, "Tolerancia")
        fichero.drawString(96 * mm, linea * mm, "Resistencia Medida")
        fichero.drawString(126 * mm, linea * mm, "Peso Nominal")
        fichero.drawString(147 * mm, linea * mm, "Tolerancia")
        fichero.drawString(165 * mm, linea * mm, "Peso Medido")
        fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
        linea = 245
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(grey)
        fichero.drawString(10 * mm, linea * mm, "Serial Number")
        #       fichero.drawString(25*mm,linea*mm, "Inael Reference")
        fichero.drawString(40 * mm, linea * mm, "Nominal Resistance")
        fichero.drawString(77 * mm, linea * mm, "Tolerance")
        fichero.drawString(96 * mm, linea * mm, "Obtained Resistance")
        fichero.drawString(126 * mm, linea * mm, "Nominal Weight")
        fichero.drawString(147 * mm, linea * mm, "Tolerance")
        fichero.drawString(165 * mm, linea * mm, "Obtained Weight")
        fichero.drawString(185 * mm, linea * mm, "Test Date")
        linea = 242
        fichero.setFillColor(red)
        fichero.setFont("Helvetica", 7)
        w_ohm = "(m" + "\u2126" + ")"
        w_masmenos = "(" + "\u00b1" + " %)"
        fichero.drawString(52 * mm, linea * mm, w_ohm)
        fichero.drawString(81 * mm, linea * mm, w_masmenos)
        fichero.drawString(103 * mm, linea * mm, w_ohm)
        fichero.drawString(132 * mm, linea * mm, "(gr)")
        fichero.drawString(151 * mm, linea * mm, w_masmenos)
        fichero.drawString(172 * mm, linea * mm, "(gr)")
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        linea = 241
        fichero.line(9 * mm, 241 * mm, 204 * mm, 241 * mm)
        fichero.line(9 * mm, 252 * mm, 9 * mm, 241 * mm)
        fichero.line(39 * mm, 252 * mm, 39 * mm, 241 * mm)
        fichero.line(76 * mm, 252 * mm, 76 * mm, 241 * mm)
        fichero.line(95 * mm, 252 * mm, 95 * mm, 241 * mm)
        fichero.line(125 * mm, 252 * mm, 125 * mm, 241 * mm)
        fichero.line(146 * mm, 252 * mm, 146 * mm, 241 * mm)
        fichero.line(164 * mm, 252 * mm, 164 * mm, 241 * mm)
        fichero.line(184 * mm, 252 * mm, 184 * mm, 241 * mm)
        fichero.line(204 * mm, 252 * mm, 204 * mm, 241 * mm)
        sw = True
        if not self.pedido_cliente:
            self.pedido_cliente = " "

        for fus in self.env["res.fusibles"].browse(self.env.context.get("active_ids")):
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", fus.product_id.id), ("ensayo_id", "=", 66)]
            )  # 66 es Nota de Pie Informe
            if ens_ids:
                if not ens_ids.nota:
                    ens_ids.nota = " "
                w_nota_pie = ens_ids.nota.strip()
            else:
                w_nota_pie = False
            if sw:
                fichero.setFont("Helvetica-Bold", 9)
                fichero.drawString(65 * mm, 257 * mm, self.pedido_cliente)
                fichero.drawString(140 * mm, 257 * mm, fus.product_id.name)
                fichero.setFont("Helvetica", 7)
                fichero.drawString(140 * mm, 254 * mm, fus.product_id.default_code)
                sw = False
            if not self.listar_rechazos:
                if (
                    fus.rechazado_resis or fus.rechazado_peso
                ):  # si esta rechazado no lo saco
                    continue
            linea -= 4
            fichero.setFont("Helvetica", 7)
            fichero.drawString(12 * mm, linea * mm, fus.num_serie)
            w_n = fus.res_nominal if fus.res_nominal else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(58 * mm, linea * mm, s_n)
            w_n = fus.tol_resis if fus.tol_resis else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(88 * mm, linea * mm, s_n)
            w_n = fus.res_medida if fus.res_medida else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(114 * mm, linea * mm, s_n)
            w_n = fus.peso_nominal if fus.peso_nominal else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(140 * mm, linea * mm, s_n)
            w_n = fus.tol_peso if fus.tol_peso else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(156 * mm, linea * mm, s_n)
            w_n = fus.peso_medido if fus.peso_medido else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(180 * mm, linea * mm, s_n)
            fec = str(fus.fecha_ensayo)
            wfecha = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
            fichero.drawString(187 * mm, linea * mm, wfecha)
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(9 * mm, linea * mm, 204 * mm, linea * mm)
            fichero.line(9 * mm, linea * mm, 9 * mm, (linea + 5) * mm)
            fichero.line(39 * mm, linea * mm, 39 * mm, (linea + 5) * mm)
            fichero.line(76 * mm, linea * mm, 76 * mm, (linea + 5) * mm)
            fichero.line(95 * mm, linea * mm, 95 * mm, (linea + 5) * mm)
            fichero.line(125 * mm, linea * mm, 125 * mm, (linea + 5) * mm)
            fichero.line(146 * mm, linea * mm, 146 * mm, (linea + 5) * mm)
            fichero.line(164 * mm, linea * mm, 164 * mm, (linea + 5) * mm)
            fichero.line(184 * mm, linea * mm, 184 * mm, (linea + 5) * mm)
            fichero.line(204 * mm, linea * mm, 204 * mm, (linea + 5) * mm)
            fichero.setStrokeColor(black)
            # salto de pagina  y  Cabecera
            if linea <= 25:
                w_pagina += 1
                self.cabecera(fichero, w_pagina)
                linea = 253
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

    def cabecera(self, fichero, w_pagina):
        fichero.showPage()
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
        fichero.setFont("Helvetica", 6)
        fichero.drawString(195 * mm, 285 * mm, "Pag. " + str(w_pagina))
        fichero.setLineWidth(2)
        #       fichero.rect(3*mm,15*mm,204*mm,255*mm)
        fichero.roundRect(
            2 * mm, 15 * mm, 205 * mm, 255 * mm, radius=5, stroke=1, fill=0
        )  # si fill=0 no rellena
        fichero.setLineWidth(1)
        linea = 264
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(9 * mm, linea * mm, 204 * mm, linea * mm)
        linea = 261
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(10 * mm, linea * mm, "Num. Serie")
        fichero.drawString(40 * mm, linea * mm, "Resistencia Nominal")
        fichero.drawString(77 * mm, linea * mm, "Tolerancia")
        fichero.drawString(96 * mm, linea * mm, "Resistencia Medida")
        fichero.drawString(126 * mm, linea * mm, "Peso Nominal")
        fichero.drawString(147 * mm, linea * mm, "Tolerancia")
        fichero.drawString(165 * mm, linea * mm, "Peso Medido")
        fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
        linea = 257
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(grey)
        fichero.drawString(10 * mm, linea * mm, "Serial Number")
        fichero.drawString(40 * mm, linea * mm, "Nominal Resistance")
        fichero.drawString(77 * mm, linea * mm, "Tolerance")
        fichero.drawString(96 * mm, linea * mm, "Obtained Resistance")
        fichero.drawString(126 * mm, linea * mm, "Nominal Weight")
        fichero.drawString(147 * mm, linea * mm, "Tolerance")
        fichero.drawString(165 * mm, linea * mm, "Obtained Weight")
        fichero.drawString(185 * mm, linea * mm, "Test Date")
        linea = 254
        fichero.setFillColor(red)
        fichero.setFont("Helvetica", 7)
        w_ohm = "(" + "\u00b5" + "\u2126" + ")"
        w_masmenos = "(" + "\u00b1" + " %)"
        fichero.drawString(52 * mm, linea * mm, w_ohm)
        fichero.drawString(81 * mm, linea * mm, w_masmenos)
        fichero.drawString(103 * mm, linea * mm, w_ohm)
        fichero.drawString(132 * mm, linea * mm, "(gr)")
        fichero.drawString(151 * mm, linea * mm, w_masmenos)
        fichero.drawString(172 * mm, linea * mm, "(gr)")
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        linea = 253
        fichero.line(9 * mm, 253 * mm, 204 * mm, 253 * mm)
        fichero.line(9 * mm, 264 * mm, 9 * mm, 253 * mm)
        fichero.line(39 * mm, 264 * mm, 39 * mm, 253 * mm)
        fichero.line(76 * mm, 264 * mm, 76 * mm, 253 * mm)
        fichero.line(95 * mm, 264 * mm, 95 * mm, 253 * mm)
        fichero.line(125 * mm, 264 * mm, 125 * mm, 253 * mm)
        fichero.line(146 * mm, 264 * mm, 146 * mm, 253 * mm)
        fichero.line(164 * mm, 264 * mm, 164 * mm, 253 * mm)
        fichero.line(184 * mm, 264 * mm, 184 * mm, 253 * mm)
        fichero.line(204 * mm, 264 * mm, 204 * mm, 253 * mm)
