# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import re

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


class WizInformeSecciona(models.TransientModel):
    _name = "wiz.informe.secciona"
    _description = "Listar Informe Secciona"

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
            raise exceptions.Warning(_("Tienes que seleccionar al menos 1 Seccionador"))
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
        """Give a format you want to extend and a dict of the properties you want
        to extend it with, and you get them returned in a single format.
        """
        new_dict = {}
        for key, value in existing_format.__dict__.items():
            if value != 0 and value != {} and value is not None:
                new_dict[key] = value
        new_dict.pop("escapes", None)
        new_dict.update(dict_of_properties)
        return workbook.add_format(new_dict)

    def export_pdf(self):
        prime = True
        produc = False
        for r in self.env["res.seccionadores"].browse(
            self.env.context.get("active_ids")
        ):
            if prime:
                prime = False
                produc = r.product_id.id
            if produc != r.product_id.id:
                raise exceptions.Warning(
                    _(
                        "Los seccionadores seleccionados tienen que tener "
                        "la misma referencia."
                    )
                )
        this = self[0]
        self.generar_pdf()
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/secciona" + "_" + w_usuario + ".pdf"
        fname = "secciona.pdf"
        modelo = "wiz.informe.secciona"
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
        fichero_name = "/tmp/secciona" + "_" + w_usuario + ".pdf"
        fichero = Canvas(fichero_name)
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        w_pagina = 0
        fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
        fichero.setLineWidth(2)
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
        fichero.drawString(6 * mm, linea * mm, "Informe de ensayos - Seccionadores")
        fichero.setFont("Helvetica-Bold", 11)
        fichero.drawString(85 * mm, linea * mm, "  Test report - Disconnectors  ")
        linea = 258
        fichero.setFont("Helvetica", 9)
        fichero.setFillColor(black)
        fichero.drawString(6 * mm, linea * mm, "Referencia Cliente")
        fichero.setFillColor(grey)
        fichero.drawString(32 * mm, linea * mm, " / Customer reference:")
        fichero.setFillColor(black)
        fichero.drawString(98 * mm, linea * mm, "Tipo ")
        fichero.setFillColor(grey)
        fichero.drawString(105 * mm, linea * mm, " / Type: ")
        fichero.setFillColor(black)
        linea = 252
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(4 * mm, linea * mm, 204 * mm, linea * mm)
        linea = 249
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(5 * mm, linea * mm, "Orden")
        fichero.drawString(25 * mm, linea * mm, "Numero de serie")
        fichero.drawString(47 * mm, linea * mm, "Control dimensional")
        fichero.drawString(76 * mm, linea * mm, "Control de contacto")
        fichero.drawString(105 * mm, linea * mm, "Control funcional")
        fichero.drawString(132 * mm, linea * mm, "Lubricacion")
        fichero.drawString(153 * mm, linea * mm, "Marcas")
        fichero.drawString(169 * mm, linea * mm, "Resistencia")
        fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
        linea = 245
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(grey)
        fichero.drawString(5 * mm, linea * mm, "Order")
        fichero.drawString(25 * mm, linea * mm, "Serial number")
        fichero.drawString(47 * mm, linea * mm, "Dimensional control")
        fichero.drawString(76 * mm, linea * mm, "Alignment of poles")
        fichero.drawString(105 * mm, linea * mm, "Functional control")
        fichero.drawString(132 * mm, linea * mm, "Lubrication")
        fichero.drawString(153 * mm, linea * mm, "Marks")
        fichero.drawString(169 * mm, linea * mm, "Resistance")
        fichero.drawString(185 * mm, linea * mm, "Test Date")
        linea = 242
        fichero.setFillColor(red)
        fichero.setFont("Helvetica", 7)
        w_ohm = "(" + "\u00b5" + "\u2126" + ")"
        fichero.drawString(172 * mm, linea * mm, w_ohm)
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        linea = 241
        fichero.line(4 * mm, 241 * mm, 204 * mm, 241 * mm)
        fichero.line(4 * mm, 252 * mm, 4 * mm, 241 * mm)
        fichero.line(24 * mm, 252 * mm, 24 * mm, 241 * mm)
        fichero.line(46 * mm, 252 * mm, 46 * mm, 241 * mm)
        fichero.line(75 * mm, 252 * mm, 75 * mm, 241 * mm)
        fichero.line(104 * mm, 252 * mm, 104 * mm, 241 * mm)
        fichero.line(129 * mm, 252 * mm, 129 * mm, 241 * mm)
        fichero.line(149 * mm, 252 * mm, 149 * mm, 241 * mm)
        fichero.line(167 * mm, 252 * mm, 167 * mm, 241 * mm)
        fichero.line(184 * mm, 252 * mm, 184 * mm, 241 * mm)
        fichero.line(204 * mm, 252 * mm, 204 * mm, 241 * mm)
        sw = True
        if not self.pedido_cliente:
            self.pedido_cliente = " "
        for sec in self.env["res.seccionadores"].browse(
            self.env.context.get("active_ids")
        ):
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", sec.product_id.id), ("ensayo_id", "=", 66)]
            )  # 66 es Nota de Pie Informe
            if ens_ids:
                if not ens_ids.nota:
                    ens_ids.nota = " "
                w_nota_pie = ens_ids.nota.strip()
            else:
                w_nota_pie = False
            if sw:
                fichero.setFont("Helvetica", 8)
                fichero.drawString(65 * mm, 258 * mm, self.pedido_cliente)
                fichero.drawString(116 * mm, 258 * mm, sec.product_id.name)
                fichero.drawString(116 * mm, 254 * mm, sec.product_id.default_code)
                sw = False
            linea -= 4
            fichero.setFont("Helvetica", 7)
            fichero.drawString(6 * mm, linea * mm, sec.production_id.name)
            fichero.drawString(25 * mm, linea * mm, sec.num_serie)
            w_ok = "\u2713"
            fichero.drawString(57 * mm, linea * mm, w_ok)
            fichero.drawString(85 * mm, linea * mm, w_ok)
            fichero.drawString(112 * mm, linea * mm, w_ok)
            fichero.drawString(138 * mm, linea * mm, w_ok)
            fichero.drawString(156 * mm, linea * mm, w_ok)
            w_n = sec.res_r_medida if sec.res_r_medida else 0
            s_n = self._puntuacion(str(f"{w_n:,.2f}"))
            fichero.drawRightString(180 * mm, linea * mm, s_n)
            fec = str(sec.fecha_ensayo)
            wfecha = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
            fichero.drawString(185 * mm, linea * mm, wfecha)
            linea -= 1
            fichero.setStrokeColor(lightgrey)
            fichero.line(4 * mm, linea * mm, 204 * mm, linea * mm)
            fichero.line(4 * mm, linea * mm, 4 * mm, (linea + 5) * mm)
            fichero.line(24 * mm, linea * mm, 24 * mm, (linea + 5) * mm)
            fichero.line(46 * mm, linea * mm, 46 * mm, (linea + 5) * mm)
            fichero.line(75 * mm, linea * mm, 75 * mm, (linea + 5) * mm)
            fichero.line(104 * mm, linea * mm, 104 * mm, (linea + 5) * mm)
            fichero.line(129 * mm, linea * mm, 129 * mm, (linea + 5) * mm)
            fichero.line(149 * mm, linea * mm, 149 * mm, (linea + 5) * mm)
            fichero.line(167 * mm, linea * mm, 167 * mm, (linea + 5) * mm)
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
        fichero.roundRect(
            2 * mm, 15 * mm, 205 * mm, 255 * mm, radius=5, stroke=1, fill=0
        )  # si fill=0 no rellena
        fichero.setLineWidth(1)
        linea = 264
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(4 * mm, linea * mm, 204 * mm, linea * mm)
        linea = 261
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(5 * mm, linea * mm, "Orden")
        fichero.drawString(25 * mm, linea * mm, "Numero de serie")
        fichero.drawString(47 * mm, linea * mm, "Control dimensional")
        fichero.drawString(76 * mm, linea * mm, "Control de contacto")
        fichero.drawString(105 * mm, linea * mm, "Control funcional")
        fichero.drawString(130 * mm, linea * mm, "Lubricacion")
        fichero.drawString(150 * mm, linea * mm, "Marcas")
        fichero.drawString(168 * mm, linea * mm, "Resistencia")
        fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
        linea = 257
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(grey)
        fichero.drawString(5 * mm, linea * mm, "Order")
        fichero.drawString(25 * mm, linea * mm, "Serial number")
        fichero.drawString(47 * mm, linea * mm, "Dimensional control")
        fichero.drawString(76 * mm, linea * mm, "Alignment of poles")
        fichero.drawString(105 * mm, linea * mm, "Functional control")
        fichero.drawString(130 * mm, linea * mm, "Lubrication")
        fichero.drawString(150 * mm, linea * mm, "Marks")
        fichero.drawString(168 * mm, linea * mm, "Resistance")
        fichero.drawString(185 * mm, linea * mm, "Test Date")
        linea = 254
        fichero.setFillColor(red)
        fichero.setFont("Helvetica", 7)
        w_ohm = "(" + "\u00b5" + "\u2126" + ")"
        fichero.drawString(172 * mm, linea * mm, w_ohm)
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        linea = 253
        fichero.line(4 * mm, 253 * mm, 204 * mm, 253 * mm)
        fichero.line(4 * mm, 264 * mm, 4 * mm, 253 * mm)
        fichero.line(24 * mm, 264 * mm, 24 * mm, 253 * mm)
        fichero.line(46 * mm, 264 * mm, 46 * mm, 253 * mm)
        fichero.line(75 * mm, 264 * mm, 75 * mm, 253 * mm)
        fichero.line(104 * mm, 264 * mm, 104 * mm, 253 * mm)
        fichero.line(129 * mm, 264 * mm, 129 * mm, 253 * mm)
        fichero.line(149 * mm, 264 * mm, 149 * mm, 253 * mm)
        fichero.line(167 * mm, 264 * mm, 167 * mm, 253 * mm)
        fichero.line(184 * mm, 264 * mm, 184 * mm, 253 * mm)
        fichero.line(204 * mm, 264 * mm, 204 * mm, 253 * mm)
