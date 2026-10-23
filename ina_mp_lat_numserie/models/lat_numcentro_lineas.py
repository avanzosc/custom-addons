# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

ENSAYO_MODELOS = {
    "aisladores": "res.aisladores",
    "celdas": "res.celdas",
    "fusibles": "res.fusibles",
    "pararrayos": "res.pararrayos",
    "selas": "res.seccionadores",
    "trafos": "res.trafos",
}


class LatNumcentroLineas(models.Model):
    _name = "lat.numcentro.lineas"
    _description = "Numeros de serie para Centros"
    _inherit = ["ina.lat.lot.mixin"]
    _lat_tracking = "lot"

    num_id = fields.Many2one(
        string="Numeros serie dia", comodel_name="lat.numcentro", ondelete="cascade"
    )
    ensayo = fields.Selection(
        [
            ("aisladores", "Aisladores"),
            ("celdas", "Celdas y OCRs"),
            ("edificio", "Edificio"),
            ("fusibles", "Fusibles"),
            ("pararrayos", "Pararrayos"),
            ("seccionalizadores", "Seccionalizadores"),
            ("selas", "Selas y Seccionadores"),
            ("trafos", "Trafos"),
            ("otros", "No Nuestro"),
        ],
    )
    numserie = fields.Char(
        string="Numero de Serie Antiguo",
        index=True,
        readonly=True,
        help="Numero de serie de los registros que no se pudieron pasar a lote "
        "por no tener producto.",
    )
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    venta_id = fields.Many2one(
        "sale.order", string="Ord. Venta", related="num_id.venta_id", store="True"
    )
    partner_id = fields.Many2one("res.partner", string="Proveedor")
    decla = fields.Boolean("DC")
    infens = fields.Boolean("IE")
    chklis = fields.Boolean("CKL")
    otros = fields.Boolean("Fichero")
    fichero = fields.Char("Fichero Externo")
    etf = fields.Boolean("ETF")
    pla = fields.Boolean("PLA")
    peso_sf6 = fields.Integer("Peso SF6")
    color_sf6 = fields.Integer("Color")  # 1 Rojo 2 Verde

    @api.onchange("lot_id")
    def onchange_lot_id(self):
        if not self.lot_id:
            return
        warning = {}
        title = False
        message = False
        for r in self:
            r.product_id = r.lot_id.product_id
            r.production_id = False
            modelo = ENSAYO_MODELOS.get(r.ensayo)
            if not modelo:
                return {}
            e_ids = self.env[modelo].search([("lot_id", "=", r.lot_id.id)], limit=1)
            if e_ids:
                r.production_id = e_ids.production_id.id
                r.peso_sf6 = 0
                r.color_sf6 = 0
                if r.ensayo == "celdas":
                    r.peso_sf6 = e_ids.peso_sf6
                    if e_ids.peso_sf6 > 0:
                        r.color_sf6 = 2
                    else:
                        r.color_sf6 = 1
            else:
                r.ensayo = "otros"
                title = "Aviso"
                message = "Numero de serie no encontrado"
                warning["title"] = title
                warning["message"] = message
                return {"warning": warning}
            num_ids = self.env["lat.numserie"].search(
                [("lot_id", "=", r.lot_id.id), ("ensayo", "=", r.ensayo)], limit=1
            )
            if num_ids:
                title = "Aviso"
                message = (
                    "Ya está puesto este número de serie en la "
                    f"{num_ids.ov} y producto {num_ids.product_id.default_code}"
                )
                warning["title"] = title
                warning["message"] = message
                r.lot_id = False
                return {"warning": warning}
        return {}
