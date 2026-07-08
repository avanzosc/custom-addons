# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class LatNumcentroLineas(models.Model):
    _name = "lat.numcentro.lineas"
    _description = "Numeros de serie para Centros"

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
    numserie = fields.Char(string="Numero de Serie", index=True, required=True)
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

    @api.onchange("numserie")
    def onchange_numserie(self):
        if not self.numserie:
            return
        warning = {}
        title = False
        message = False
        for r in self:
            r.product_id = r.production_id = False
            if r.ensayo == "celdas":
                if not r.numserie.isdigit():
                    raise exceptions.Warning(_("Solo se admiten numeros"))
                e_obj = self.env["res.celdas"]
                cond = [("celda_num", "=", r.numserie)]
            elif r.ensayo == "fusibles":
                e_obj = self.env["res.fusibles"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.ensayo == "selas":
                e_obj = self.env["res.seccionadores"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.ensayo == "pararrayos":
                if not r.numserie.isdigit():
                    raise exceptions.Warning(_("Solo se admiten numeros"))
                e_obj = self.env["res.pararrayos"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.ensayo == "aisladores":
                if not r.numserie.isdigit():
                    raise exceptions.Warning(_("Solo se admiten numeros"))
                e_obj = self.env["res.aisladores"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.ensayo == "trafos":
                r.ensayo = "otros"
            else:
                return {}
            e_ids = e_obj.search(cond, limit=1)
            if e_ids:
                r.production_id = e_ids.production_id.id
                r.product_id = e_ids.product_id.id
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
                [("numserie", "=", r.numserie), ("ensayo", "=", r.ensayo)], limit=1
            )
            if num_ids:
                title = "Aviso"
                message = (
                    "Ya está puesto este número de serie en la "
                    f"{num_ids.ov} y producto {num_ids.product_id.default_code}"
                )
                warning["title"] = title
                warning["message"] = message
                r.numserie = False
                return {"warning": warning}
        return {}
