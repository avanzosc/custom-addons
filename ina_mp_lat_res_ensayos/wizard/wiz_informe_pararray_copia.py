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
from reportlab.lib.pagesizes import A4, landscape
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


class WizInformePararray(models.TransientModel):
    _name = "wiz.informe.pararray"
    _description = "Listar Informe Pararrayos"

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    state = fields.Selection(
        [("choose", "choose"), ("get", "get")],  # choose language or get the file
        default="choose",
    )
    pedido_cliente = fields.Char()
    listar_rechazos = fields.Boolean(default=False)
    informe_tipo = fields.Boolean(string="Informe de Conjunto", default=False)

    @api.model
    def _dirty_check(self):
        ids = self.env.context["active_ids"]
        if not self.informe_tipo:
            if len(ids) < 1:
                raise exceptions.Warning(
                    _("Tienes que seleccionar al menos 1 Pararrayos")
                )
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

    @api.multi
    def export_pdf(self):
        if not self.informe_tipo:
            prime = True
            produc = False
            for r in self.env["res.pararrayos"].browse(
                self.env.context.get("active_ids")
            ):
                if prime:
                    prime = False
                    produc = r.product_id.id
                if produc != r.product_id.id:
                    raise exceptions.Warning(
                        _(
                            "Los Pararrayos seleccionados tienen que tener "
                            "la misma referencia."
                        )
                    )
        this = self[0]
        self.generar_pdf()
        w_usuario = (self.env.user.login).strip()
        fichero_name = "/tmp/pararray" + "_" + w_usuario + ".pdf"
        fname = "pararray.pdf"
        modelo = "wiz.informe.pararray"
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
        fichero_name = "/tmp/pararray" + "_" + w_usuario + ".pdf"
        #       fichero= (fichero_name)
        if self.informe_tipo:
            fichero = Canvas(
                fichero_name, pagesize=landscape(A4)
            )  # para listar en horizontal
        else:
            fichero = Canvas(fichero_name)
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        tz = pytz.timezone("Europe/Madrid")
        fec0 = fields.datetime.now(tz)
        fec = str(fec0)
        w_pagina = 0
        if self.informe_tipo:
            fichero.drawImage(logo3, 0, 0, width=820, height=595)  # en 580 tenia 600
        else:
            fichero.drawImage(logo3, 0, 0, width=593, height=843)  # en 580 tenia 600
        fichero.setLineWidth(1)
        fichero.setFont("Helvetica", 6)
        w_pagina += 1
        fichero.setFillColor(black)
        if not self.informe_tipo:
            fichero.setFont("Helvetica", 6)
            fichero.drawString(195 * mm, 285 * mm, "Pag. " + str(w_pagina))
            linea = 264
            fichero.setFillColor(black)
            fichero.setFont("Helvetica-Bold", 12)
            fichero.drawString(6 * mm, linea * mm, "Informe de ensayos - Pararrayos")
            fichero.setFont("Helvetica-Bold", 11)
            fichero.drawString(85 * mm, linea * mm, "  Test report - Arresters  ")
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
            fichero.drawString(20 * mm, linea * mm, "Numero de serie")
            fichero.drawString(42 * mm, linea * mm, "Potencia (W) a Uc")
            fichero.drawString(68 * mm, linea * mm, "Corriente de Referencia")
            fichero.drawString(98 * mm, linea * mm, "Tension de Referencia (kV pico)")
            fichero.drawString(145 * mm, linea * mm, "Nivel de Descargas Parciales")
            fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
            linea = 245
            fichero.drawString(68 * mm, linea * mm, "(mA pico)")
            fichero.drawString(98 * mm, linea * mm, "a Corriente de Referencia")
            fichero.drawString(145 * mm, linea * mm, "a 1,05*Uc (pC)")
            linea = 241
            fichero.setFont("Helvetica", 7)
            fichero.setFillColor(grey)
            fichero.drawString(5 * mm, linea * mm, "Order")
            fichero.drawString(20 * mm, linea * mm, "Serial number")
            fichero.drawString(42 * mm, linea * mm, "Power (W) at Uc")
            fichero.drawString(68 * mm, linea * mm, "Reference Current")
            fichero.drawString(98 * mm, linea * mm, "Reference Voltage (kV peak) ")
            fichero.drawString(145 * mm, linea * mm, "Partial Discharge Level")
            fichero.drawString(185 * mm, linea * mm, "Test Date")
            linea = 238
            fichero.drawString(68 * mm, linea * mm, "(mA peak)")
            fichero.drawString(98 * mm, linea * mm, "at Reference Current")
            fichero.drawString(145 * mm, linea * mm, "at 1,05*Uc (pC)")
            fichero.setFillColor(black)
            fichero.setLineWidth(1)
            linea = 236
            fichero.line(4 * mm, 236 * mm, 204 * mm, 236 * mm)
            fichero.line(4 * mm, 252 * mm, 4 * mm, 236 * mm)
            fichero.line(19 * mm, 252 * mm, 19 * mm, 236 * mm)
            fichero.line(40 * mm, 252 * mm, 40 * mm, 236 * mm)
            fichero.line(66 * mm, 252 * mm, 66 * mm, 236 * mm)
            fichero.line(96 * mm, 252 * mm, 96 * mm, 236 * mm)
            fichero.line(143 * mm, 252 * mm, 143 * mm, 236 * mm)
            fichero.line(183 * mm, 252 * mm, 183 * mm, 236 * mm)
            fichero.line(204 * mm, 252 * mm, 204 * mm, 233 * mm)
        else:
            linea = 196
            fichero.setFont("Helvetica", 6)
            fichero.drawString(280 * mm, linea * mm, "Pag. " + str(w_pagina))
            fichero.setFont("Helvetica-Bold", 11)
            fichero.drawString(
                85 * mm, linea * mm, "Informe de ensayos - Conjunto de Pararrayos"
            )
            linea = 190
            fichero.setFont("Helvetica", 10)
            fichero.setFillColor(black)
            fichero.drawString(90 * mm, linea * mm, "Referencia Cliente:")
            linea = 185
            fichero.setFillColor(black)
            fichero.setLineWidth(1)
            fichero.line(4 * mm, linea * mm, 290 * mm, linea * mm)
            linea = 182
            fichero.setFont("Helvetica", 7)
            fichero.setFillColor(red)
            fichero.drawString(5 * mm, linea * mm, "N. Serie")
            fichero.drawString(25 * mm, linea * mm, "Producto")
            fichero.drawString(91 * mm, linea * mm, "Potencia ")
            fichero.drawString(115 * mm, linea * mm, "Corriente ")
            fichero.drawString(145 * mm, linea * mm, "Tension de ")
            fichero.drawString(175 * mm, linea * mm, "Riv ")
            fichero.drawString(200 * mm, linea * mm, "Corona ")
            fichero.drawString(220 * mm, linea * mm, "Fecha Ensayo")
            fichero.drawString(240 * mm, linea * mm, "Orden Conjunto")
            fichero.drawString(265 * mm, linea * mm, "Num. Serie Conjunto")
            linea -= 4
            fichero.drawString(91 * mm, linea * mm, "Ensayada")
            fichero.drawString(115 * mm, linea * mm, "Ensayada")
            fichero.drawString(145 * mm, linea * mm, "Referencia")
            fichero.drawString(172 * mm, linea * mm, "Ensayada")
            fichero.drawString(200 * mm, linea * mm, "Ensayada")
            linea -= 1
            fichero.setFillColor(black)
            fichero.setLineWidth(1)
            fichero.line(4 * mm, linea * mm, 290 * mm, linea * mm)
            fichero.line(4 * mm, linea * mm, 4 * mm, (linea + 8) * mm)
            fichero.line(19 * mm, linea * mm, 19 * mm, (linea + 8) * mm)
            fichero.line(85 * mm, linea * mm, 85 * mm, (linea + 8) * mm)
            fichero.line(110 * mm, linea * mm, 110 * mm, (linea + 8) * mm)
            fichero.line(140 * mm, linea * mm, 140 * mm, (linea + 8) * mm)
            fichero.line(170 * mm, linea * mm, 170 * mm, (linea + 8) * mm)
            fichero.line(196 * mm, linea * mm, 196 * mm, (linea + 8) * mm)
            fichero.line(218 * mm, linea * mm, 218 * mm, (linea + 8) * mm)
            fichero.line(239 * mm, linea * mm, 239 * mm, (linea + 8) * mm)
            fichero.line(264 * mm, linea * mm, 264 * mm, (linea + 8) * mm)
            fichero.line(290 * mm, linea * mm, 290 * mm, (linea + 8) * mm)
        sw = True
        if not self.pedido_cliente:
            self.pedido_cliente = " "
        for par in self.env["res.pararrayos"].browse(
            self.env.context.get("active_ids")
        ):
            ens_ids = self.env["mrp.ensayos.producto"].search(
                [("product_id", "=", par.product_id.id), ("ensayo_id", "=", 66)]
            )  # 66 es Nota de Pie Informe
            if ens_ids:
                if not ens_ids.nota:
                    ens_ids.nota = " "
                w_nota_pie = ens_ids.nota.strip()
            else:
                w_nota_pie = False
            if sw:
                fichero.setFont("Helvetica", 8)
                if not self.informe_tipo:
                    fichero.drawString(65 * mm, 258 * mm, self.pedido_cliente)
                    fichero.drawString(116 * mm, 258 * mm, par.product_id.name)
                    fichero.drawString(116 * mm, 254 * mm, par.product_id.default_code)
                else:
                    fichero.drawString(122 * mm, 190 * mm, self.pedido_cliente)
                sw = False
            linea -= 4
            if not self.informe_tipo:
                fichero.setFont("Helvetica", 7)
                fichero.drawString(5 * mm, linea * mm, par.production_id.name)
                w_n = par.num_serie if par.num_serie else 0
                s_n0 = self._puntuacion(str(f"{w_n:,.0f}"))
                s_n = s_n0.replace(".", "")
                fichero.drawString(20 * mm, linea * mm, s_n)
                w_n = par.poten_ensa if par.poten_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.3f}"))
                fichero.drawRightString(54 * mm, linea * mm, s_n)
                w_n = par.corri_ensa if par.corri_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.3f}"))
                fichero.drawRightString(80 * mm, linea * mm, s_n)
                w_n = par.tensi_refer if par.tensi_refer else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(115 * mm, linea * mm, s_n)
                w_n = par.coro_ensa if par.coro_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(160 * mm, linea * mm, s_n)
                fec = str(par.fecha_ensayo)
                wfecha = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
                fichero.drawString(185 * mm, linea * mm, wfecha)
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(4 * mm, linea * mm, 204 * mm, linea * mm)
                fichero.line(4 * mm, linea * mm, 4 * mm, (linea + 5) * mm)
                fichero.line(19 * mm, linea * mm, 19 * mm, (linea + 5) * mm)
                fichero.line(40 * mm, linea * mm, 40 * mm, (linea + 5) * mm)
                fichero.line(66 * mm, linea * mm, 66 * mm, (linea + 5) * mm)
                fichero.line(96 * mm, linea * mm, 96 * mm, (linea + 5) * mm)
                fichero.line(143 * mm, linea * mm, 143 * mm, (linea + 5) * mm)
                fichero.line(183 * mm, linea * mm, 183 * mm, (linea + 5) * mm)
                fichero.line(204 * mm, linea * mm, 204 * mm, (linea + 5) * mm)
            else:
                fichero.setFont("Helvetica", 6)
                w_n = par.num_serie if par.num_serie else 0
                s_n0 = self._puntuacion(str(f"{w_n:,.0f}"))
                s_n = s_n0.replace(".", "")
                fichero.drawString(5 * mm, linea * mm, s_n)
                fichero.drawString(20 * mm, linea * mm, par.product_id.display_name)
                fichero.setFont("Helvetica", 7)
                w_n = par.poten_ensa if par.poten_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.3f}"))
                fichero.drawRightString(100 * mm, linea * mm, s_n)
                w_n = par.corri_ensa if par.corri_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.3f}"))
                fichero.drawRightString(123 * mm, linea * mm, s_n)
                w_n = par.tensi_refer if par.tensi_refer else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(155 * mm, linea * mm, s_n)
                w_n = par.riv_ensa if par.riv_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(183 * mm, linea * mm, s_n)
                w_n = par.coro_ensa if par.coro_ensa else 0
                s_n = self._puntuacion(str(f"{w_n:,.2f}"))
                fichero.drawRightString(207 * mm, linea * mm, s_n)
                fec = str(par.fecha_ensayo)
                wfecha = fec[8:10] + "/" + fec[5:7] + "/" + fec[0:4]
                fichero.drawString(222 * mm, linea * mm, wfecha)
                fichero.drawString(243 * mm, linea * mm, par.orden_conjunto.name)
                fichero.drawString(270 * mm, linea * mm, par.num_serie_conj)
                linea -= 1
                fichero.setStrokeColor(lightgrey)
                fichero.line(4 * mm, linea * mm, 290 * mm, linea * mm)
                fichero.line(4 * mm, linea * mm, 4 * mm, (linea + 5) * mm)
                fichero.line(19 * mm, linea * mm, 19 * mm, (linea + 5) * mm)
                fichero.line(85 * mm, linea * mm, 85 * mm, (linea + 5) * mm)
                fichero.line(110 * mm, linea * mm, 110 * mm, (linea + 5) * mm)
                fichero.line(140 * mm, linea * mm, 140 * mm, (linea + 5) * mm)
                fichero.line(170 * mm, linea * mm, 170 * mm, (linea + 5) * mm)
                fichero.line(196 * mm, linea * mm, 196 * mm, (linea + 5) * mm)
                fichero.line(218 * mm, linea * mm, 218 * mm, (linea + 5) * mm)
                fichero.line(239 * mm, linea * mm, 239 * mm, (linea + 5) * mm)
                fichero.line(264 * mm, linea * mm, 264 * mm, (linea + 5) * mm)
                fichero.line(290 * mm, linea * mm, 290 * mm, (linea + 5) * mm)
            fichero.setStrokeColor(black)
            # salto de pagina  y  Cabecera
            if not self.informe_tipo:
                if linea <= 25:
                    w_pagina += 1
                    self.cabecera(fichero, w_pagina)
                    linea = 248
            else:
                if linea <= 30:
                    w_pagina += 1
                    self.cabecera_conjunto(fichero, w_pagina)
                    linea = 177
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
        linea = 7
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
        fichero.setLineWidth(1)
        linea = 264
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(4 * mm, linea * mm, 204 * mm, linea * mm)
        linea = 261
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(5 * mm, linea * mm, "Orden")
        fichero.drawString(20 * mm, linea * mm, "Numero de serie")
        fichero.drawString(42 * mm, linea * mm, "Potencia (W) a Uc")
        fichero.drawString(68 * mm, linea * mm, "Corriente de Referencia")
        fichero.drawString(98 * mm, linea * mm, "Tension de Referencia (kV pico)")
        fichero.drawString(145 * mm, linea * mm, "Nivel de Descargas Parciales")
        fichero.drawString(185 * mm, linea * mm, "Fecha Ensayo")
        linea = 257
        fichero.drawString(68 * mm, linea * mm, "(mA pico)")
        fichero.drawString(98 * mm, linea * mm, "a Corriente de Referencia")
        fichero.drawString(145 * mm, linea * mm, "a 1,05*Uc (pC)")
        linea = 253
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(grey)
        fichero.drawString(5 * mm, linea * mm, "Order")
        fichero.drawString(20 * mm, linea * mm, "Serial number")
        fichero.drawString(42 * mm, linea * mm, "Power (W) at Uc")
        fichero.drawString(68 * mm, linea * mm, "Reference Current")
        fichero.drawString(98 * mm, linea * mm, "Reference Voltage (kV peak) ")
        fichero.drawString(145 * mm, linea * mm, "Partial Discharge Level")
        fichero.drawString(185 * mm, linea * mm, "Test Date")
        linea = 250
        fichero.drawString(68 * mm, linea * mm, "(mA peak)")
        fichero.drawString(98 * mm, linea * mm, "at Reference Current")
        fichero.drawString(145 * mm, linea * mm, "at 1,05*Uc (pC)")
        linea = 248
        fichero.line(4 * mm, 248 * mm, 204 * mm, 248 * mm)
        fichero.line(4 * mm, 264 * mm, 4 * mm, 248 * mm)
        fichero.line(18 * mm, 264 * mm, 18 * mm, 248 * mm)
        fichero.line(40 * mm, 264 * mm, 40 * mm, 248 * mm)
        fichero.line(66 * mm, 264 * mm, 66 * mm, 248 * mm)
        fichero.line(96 * mm, 264 * mm, 96 * mm, 248 * mm)
        fichero.line(143 * mm, 264 * mm, 143 * mm, 248 * mm)
        fichero.line(183 * mm, 264 * mm, 183 * mm, 248 * mm)
        fichero.line(204 * mm, 264 * mm, 204 * mm, 248 * mm)

    def cabecera_conjunto(self, fichero, w_pagina):
        fichero.showPage()
        logo3 = ImageReader("/opt/logos/Hoja_Inael.png")
        fichero.drawImage(logo3, 0, 0, width=820, height=595)  # en 580 tenia 600
        fichero.setLineWidth(1)
        fichero.setFillColor(black)
        linea = 196
        fichero.setFont("Helvetica", 6)
        fichero.drawString(280 * mm, linea * mm, "Pag. " + str(w_pagina))
        fichero.setFont("Helvetica-Bold", 11)
        fichero.drawString(
            85 * mm, linea * mm, "Informe de ensayos - Conjunto de Pararrayos"
        )
        linea = 190
        fichero.setFont("Helvetica", 10)
        fichero.setFillColor(black)
        fichero.drawString(90 * mm, linea * mm, "Referencia Cliente:")
        fichero.drawString(122 * mm, 190 * mm, self.pedido_cliente)
        linea = 185
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(4 * mm, linea * mm, 290 * mm, linea * mm)
        linea = 182
        fichero.setFont("Helvetica", 7)
        fichero.setFillColor(red)
        fichero.drawString(5 * mm, linea * mm, "N. Serie")
        fichero.drawString(25 * mm, linea * mm, "Producto")
        fichero.drawString(91 * mm, linea * mm, "Potencia ")
        fichero.drawString(115 * mm, linea * mm, "Corriente ")
        fichero.drawString(145 * mm, linea * mm, "Tension de ")
        fichero.drawString(175 * mm, linea * mm, "Riv ")
        fichero.drawString(200 * mm, linea * mm, "Corona ")
        fichero.drawString(220 * mm, linea * mm, "Fecha Ensayo")
        fichero.drawString(240 * mm, linea * mm, "Orden Conjunto")
        fichero.drawString(265 * mm, linea * mm, "Num. Serie Conjunto")
        linea -= 4
        fichero.drawString(91 * mm, linea * mm, "Ensayada")
        fichero.drawString(115 * mm, linea * mm, "Ensayada")
        fichero.drawString(145 * mm, linea * mm, "Referencia")
        fichero.drawString(172 * mm, linea * mm, "Ensayada")
        fichero.drawString(200 * mm, linea * mm, "Ensayada")
        linea -= 1
        fichero.setFillColor(black)
        fichero.setLineWidth(1)
        fichero.line(4 * mm, linea * mm, 290 * mm, linea * mm)
        fichero.line(4 * mm, linea * mm, 4 * mm, (linea + 8) * mm)
        fichero.line(19 * mm, linea * mm, 19 * mm, (linea + 8) * mm)
        fichero.line(85 * mm, linea * mm, 85 * mm, (linea + 8) * mm)
        fichero.line(110 * mm, linea * mm, 110 * mm, (linea + 8) * mm)
        fichero.line(140 * mm, linea * mm, 140 * mm, (linea + 8) * mm)
        fichero.line(170 * mm, linea * mm, 170 * mm, (linea + 8) * mm)
        fichero.line(196 * mm, linea * mm, 196 * mm, (linea + 8) * mm)
        fichero.line(218 * mm, linea * mm, 218 * mm, (linea + 8) * mm)
        fichero.line(239 * mm, linea * mm, 239 * mm, (linea + 8) * mm)
        fichero.line(264 * mm, linea * mm, 264 * mm, (linea + 8) * mm)
        fichero.line(290 * mm, linea * mm, 290 * mm, (linea + 8) * mm)
