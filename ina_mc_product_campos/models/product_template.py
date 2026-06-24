# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends("bom_ids", "bom_ids.type")
    def _compute_fantasma(self):
        for r in self:
            r.fantasma = False
            for bom in r.bom_ids:
                if bom.type == "phantom":
                    r.fantasma = True
                else:
                    r.fantasma = False

    comision = fields.Char()
    lote = fields.Float(copy=False)
    stock_seguridad = fields.Float(
        string="Stock de Seguridad",
        help="Stock de Seguridad para MRP y/o Punto de Pedido",
        copy=False,
    )
    punto_pedido = fields.Float(
        string="Punto de Pedido",
        help="Si > 0 se calculara sugerencias de punto pedido",
        copy=False,
    )
    ud_estructura = fields.Float(string="Unidad de estructura")
    ud_ruta = fields.Float(string="Unidad de ruta")
    fantasma = fields.Boolean(compute="_compute_fantasma", store=True)
    proveedor = fields.Char()
    nota_articulo = fields.Text(string="Nota del Articulo", copy=False)
    plano = fields.Char(size=15, copy=False)
    norma = fields.Char(size=30, copy=False)
    revision_actual = fields.Char(string="Revision Articulo", size=12, copy=False)
    revision_id = fields.One2many(
        comodel_name="product.revision", inverse_name="product_id", string="Revision"
    )
    agrupa_pedido = fields.Integer(
        strig="Semanas para agrupar Ordenes",
        help="Semanas para agrupar Compras o Fabricacion",
    )
    netea_mps = fields.Boolean(
        string="Netear MPS",
        default=False,
        help="Si se marca Netear MPS, la diferencia entre MPS y ventas del "
        "periodo (semana), se pasan a la siguiente.",
    )
    barcode = fields.Char(
        string="Barcode",
        oldname="ean13",
        related="default_code",
        readonly=True,
        copy=False,
    )
    tipo_comp_fab = fields.Selection(
        [
            ("comprado", "Comprado"),
            ("fabricado", "Fabricado"),
            ("subcontratado", "Subcontratado"),
            ("corte", "Corte Laser"),
        ],
        string="Producto sera ",
        default="comprado",
    )
    producto_abc = fields.Selection(
        [("a", "A"), ("b", "B"), ("c", "C")],
        string="Producto A,B,C",
        default="c",
        copy=False,
    )
    bloqueado_sugerencia = fields.Boolean(
        string="Bloqueado para sugerencias",
        default=False,
        help="No permite crear una OC u OF desde sugerencias",
        copy=False,
    )
    inspeccion_oc = fields.Boolean(
        string="Inspeccionar OC's",
        default=False,
        help="Si se marca se tendra que autorizar la OC's antes de poder "
        "recepcionar la OC.",
    )
    nota_calidad = fields.Text(string="Nota de Calidad", copy=False)
    nota_id = fields.One2many(
        comodel_name="product.ina.nota",
        inverse_name="product_tmpl_id",
        string="Nota Factura",
        copy=False,
    )
    incluir_nota_fra_en_fabrica = fields.Boolean(
        string="Incluir Nota en OF",
        help="Lista la nota de factura tambien en OFs",
        copy=False,
    )
    planilla = fields.Char(copy=False)
    especi_tec = fields.Char(string="ET", help="Especificacion Tecnica", copy=False)
    especi_tec_fab = fields.Char(
        string="ETF", help="Especificacion Tecnica Fabricante", copy=False
    )
    manu_instru = fields.Char(string="Manual Instrucciones", copy=False)
    distri_coste = fields.Boolean(
        string="Distribuir Costes",
        default=False,
        help="Si se marca, se creara una linea de distribucion de coste cuando"
        " se recepcione",
        copy=False,
    )
    funciones = fields.Integer(default=1, help="Funciones para operativa de tiempos")
    tiempo_chapa = fields.Float(
        string="Tiempo chapa",
        digits=(9, 2),
        help="Tiempo en minutos de corte chapa en Laser",
    )
    plazo_entrega = fields.Integer(
        string="Plazo de Entrega", help="Plazo de entrega para punto de pedido"
    )
    plano_cliente = fields.Char(string="Plano de Cliente", copy=False)
    product_gas_id = fields.Many2one(
        comodel_name="product.product",
        string="Referencia Gas en corte laser",
        help="Producto de gas utilizado en esta MP de chapa para corte laser",
    )
    peso_gas = fields.Float(
        string="Peso Gas laser",
        digits=dp.get_precision("Product Unit of Measure"),
        copy=False,
        help="Peso del gas utilizado para cortar este producto. Se pondra "
        "solamente en el producto resultante que se introduce en la "
        "distribucion de corte.",
    )
    dias_fabricacion = fields.Integer(
        help="Dias de fabricacion del producto donde se utiliza."
    )
    tipo_material = fields.Char(string="Tipo de Material")
    espesor = fields.Float(digits=(9, 4), copy=False)
    volume = fields.Float(
        string="Volumen (m3)", help="The volume in m3.", digits=(9, 4)
    )
    weight = fields.Float(
        digits=(9, 4),
        help="The weight of the contents in Kg, not including any packaging, etc.",
    )
    lote_eoq = fields.Float(
        string="Lote Economico Optimo EOQ", digits=(9, 2), copy=False
    )
    material_critico = fields.Selection(
        [
            ("brugg", "Brugg"),
            ("celdaen", "Celdas Endesa"),
            ("celdai", "Celdas I-DE"),
            ("celdagnf", "Celdas GNF"),
            ("celdacon", "Celdas/Conjunto Celdas"),
            ("centros", "Centros"),
            ("china", "China"),
            ("disyuntores", "Disyuntores"),
            ("fusi", "Fusibles"),
            ("inexten", "Inext Endesa"),
            ("inextgnf", "Inext GNF"),
            ("ocr", "OCR I-DE"),
            ("para", "Pararrayos"),
            ("pintu", "Pintura/Serigrafia"),
            ("galva", "Galvanizados"),
            ("bano", "Baños"),
            ("seccionaliz", "Seccionalizadores"),
            ("inextenelchile", "INEXT ENEL CHILE"),
            ("aparellaje", "Aparellaje"),
        ],
        string="Material critico ",
        copy=False,
    )
    program1 = fields.Char(string="Program 1")
    program2 = fields.Char(string="Program 2")
    declara_conformi = fields.Char(string="Declaracion Conformidad", copy=False)
    hoja_fabrica = fields.Char(string="Hoja de Fabricacion", copy=False)
    largo = fields.Float(string="Largo (m)", digits=(9, 2))
    ancho = fields.Float(string="Ancho (m)", digits=(9, 2))
    alto = fields.Float(string="Alto  (m)", digits=(9, 2))
    inspeccion_of = fields.Boolean(
        string="Inspeccionar OF's",
        default=False,
    )
    nota_etiqueta = fields.Text(string="Nota de Etiqueta", copy=False)
    ficha_seguri = fields.Char(string="Ficha Seguridad", copy=False)
    product_reparacion_ids = fields.One2many(
        comodel_name="product.reparacion",
        inverse_name="product_id",
        string="Materiales Reparacion",
    )
    etiqueta_cable = fields.Boolean(string="Etiqueta Cableado", default=False)
    bloqueado_product = fields.Boolean(string="Prod. Bloqueado", copy=False)
    cant_pallet = fields.Float(string="Cantidad Pallet")
    uni_base = fields.Float(string="Unidades Base")
    capas_pallet = fields.Float()
    peso = fields.Float(string="Peso (kg)")
    volumen = fields.Float(string="Volumen (m3)")
    largo_pallet = fields.Float(string="Largo (m)")
    ancho_pallet = fields.Float(string="Ancho (m)")
    alto_pallet = fields.Float(string="Alto (m)")
    cbam = fields.Boolean(string="CBAM", default=False)
    rohs_raee = fields.Boolean(string="Rohs&Raee", default=False)
    unidad_embalaje = fields.Integer(string="Unidad de Embalaje")

    @api.onchange("largo")
    def onchange_largo(self):
        self.volume = self.largo * self.ancho * self.alto

    @api.onchange("ancho")
    def onchange_ancho(self):
        self.volume = self.largo * self.ancho * self.alto

    @api.onchange("alto")
    def onchange_alto(self):
        self.volume = self.largo * self.ancho * self.alto

    # Calculo del Volumen Pallet

    @api.onchange("largo_pallet")
    def onchange_largo_pallet(self):
        self.volumen = self.largo_pallet * self.ancho_pallet * self.alto_pallet

    @api.onchange("ancho_pallet")
    def onchange_ancho_pallet(self):
        self.volumen = self.largo_pallet * self.ancho_pallet * self.alto_pallet

    @api.onchange("alto_pallet")
    def onchange_alto_pallet(self):
        self.volumen = self.largo_pallet * self.ancho_pallet * self.alto_pallet


#   @api.onchange("default_code")
#   def onchange_barcode(self):
#       self.ensure_one()
#      res = super(ProductProduct, self).onchange_barcode()
#       self.barcode=self.default_code
