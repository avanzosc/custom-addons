# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import shutil
import subprocess

from odoo import api, fields, models


class LatNumcentro(models.Model):
    _name = "lat.numcentro"
    _description = "Nunmeros serie Centros"

    @api.depends("default_code")
    def _compute_producto(self):
        for r in self:
            if not r.default_code:
                return
            prod_id = self.env["product.product"].search(
                [("default_code", "=", r.default_code)], limit=1
            )
            r.product_id = prod_id.id
            if not r.product_id:
                return

    default_code = fields.Char(string="Referencia", required=True)
    venta_id = fields.Many2one(string="Ord. Venta", comodel_name="sale.order")
    product_id = fields.Many2one(
        string="Producto",
        comodel_name="product.product",
        compute="_compute_producto",
        store=True,
    )
    lineas_ids = fields.One2many(
        string="Lineas de Productos incluidos en Centro",
        comodel_name="lat.numcentro.lineas",
        inverse_name="num_id",
    )
    numserie = fields.Char(string="Numero de Serie", index=True, required=True)
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    venta_name_id = fields.Char("OV", related="venta_id.name")
    nota = fields.Text()
    insta_celdas = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Instalacion Celdas",
    )
    monta_equipo = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Montaje Equipos",
    )
    monta_tierra = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Montaje Tierras",
    )
    caja_herraje = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")], string="Caja Herrajes"
    )
    monta_cerrad = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Montaje Cerradura",
    )
    monta_puerta = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Montaje Puertas",
    )
    termo_trafo = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Termometro Trafo",
    )
    sondas_trafo = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
    )
    mega_tierras = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Megado de Tierras",
    )
    pintu_exteri = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Pintura Exterior",
    )
    pintu_interi = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Pintura Interior",
    )
    limpi_genera = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Limpieza General",
    )
    documentacio = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")], string="Documentacion"
    )
    manom_sf6 = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Manometros SF6",
    )
    enclavamien = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Enclavamientos",
    )
    llave_centro = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")], string="Llaves centro"
    )
    palan_maniob = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
        string="Palanca Maniobras",
    )
    guantes = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
    )
    banqueta = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")]
    )
    extintor = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
    )
    carteleria = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
    )
    alumbrado = fields.Selection(
        [("ok", "Ok"), ("nook", "No OK"), ("noap", "No Aplica")],
    )
    nota_noblejas = fields.Text(
        string="Observaciones",
        default="Aislamiento de tierras interiores con parámetros exteriores: "
        ">10000Ω RESULTADO FAVORABLE",
    )
    fecha_noblejas = fields.Datetime(string="Fecha Inspeccion")
    fecha_docu_genera = fields.Datetime(string="Dctos. generados el")

    @api.onchange("venta_id")
    def onchange_venta_id(self):
        if not self.venta_id:
            return
        warning = {}
        title = False
        message = False
        for r in self:
            lin_ids = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", r.venta_id.id),
                    ("product_id", "=", r.product_id.id),
                ],
                limit=1,
            )
            if not lin_ids:
                title = "Aviso"
                message = "La referencia del centro no está en la " f"{r.venta_id.name}"
                warning["title"] = title
                warning["message"] = message
                r.numserie = False
                r.ov = False
                r.product_id = False
                return {"warning": warning}
        return {}

    @api.onchange("production_id")
    def onchange_production_id(self):
        if not self.production_id:
            return
        warning = {}
        title = False
        message = False
        for r in self:
            lin_ids = self.env["mrp.production"].browse(r.production_id.id)
            if lin_ids.product_id != r.product_id:
                title = "Aviso"
                message = (
                    "La referencia del centro no está en la " f"{r.production_id.name}"
                )
                warning["title"] = title
                warning["message"] = message
                r.production_id = False
                return {"warning": warning}
        return {}

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
        self.fecha_docu_genera = fields.Datetime.now()
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

        # Busco ETF
        ruta_origen = "/media/in/Documentacion/ET de fabricantes"
        lineas = self.lineas_ids.filtered(
            lambda x: x.product_id and x.product_id.especi_tec_fab
        )
        for linea in lineas:
            patron = "*" + linea.product_id.especi_tec_fab.strip() + "*"
            encontrado = self.buscar_dto(ruta_origen, patron)
            if encontrado:
                linea.etf = True

        # Busco Planilla
        ruta_origen = "/media/in/Documentacion/Planillas"
        lineas = self.lineas_ids.filtered(
            lambda x: x.product_id and x.product_id.planilla
        )
        for linea in lineas:
            patron = "*" + linea.product_id.planilla.strip() + "*"
            encontrado = self.buscar_dto(ruta_origen, patron)
            if encontrado:
                linea.pla = True

        # Busco Otros
        ruta_origen = "/media/in/Documentacion/Documentacion_protocolos_celdas_centros"
        lineas = self.lineas_ids.filtered(lambda x: x.fichero)
        for linea in lineas:
            patron = "*" + linea.fichero.strip() + "*"
            encontrado = linea.buscar_dto(ruta_origen, patron)
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
