# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class LatNumserie(models.Model):
    _name = "lat.numserie"
    _description = "Numeros de serie para OV"

    num_id = fields.Many2one(
        string="Numeros serie dia", comodel_name="lat.num", ondelete="cascade"
    )
    numserie = fields.Char(string="Numero de Serie", index=True)
    product_id = fields.Many2one(string="Producto", comodel_name="product.product")
    venta_id = fields.Many2one(string="Ord. Venta", comodel_name="sale.order")
    production_id = fields.Many2one(
        string="Orden de Fabricacion", comodel_name="mrp.production"
    )
    linea_venta_id = fields.Many2one(
        string="Linea O.V.", comodel_name="sale.order.line"
    )
    ensayo = fields.Selection(
        [
            ("aisladores", "Aisladores"),
            ("celdas", "Celdas y OCRs"),
            ("centros", "Centros"),
            ("fusibles", "Fusibles"),
            ("pararrayos", "Pararrayos"),
            ("seccionalizadores", "Seccionalizadores"),
            ("selas", "Selas y Seccionadores"),
            ("trafos", "Trafos"),
        ],
        string="Ensayo",
        related="num_id.ensayo",
        store="True",
    )
    ov = fields.Char(string="OV", related="venta_id.name")
    decla = fields.Boolean(string="DC")
    infens = fields.Boolean(string="IE")
    chklis = fields.Boolean(string="CKL")
    otros = fields.Boolean(string="Fichero")
    fichero = fields.Char(string="Fichero Externo")
    peso_sf6 = fields.Integer(string="Peso SF6")

    @api.onchange("numserie")
    def onchange_numserie(self):
        if not self.numserie:
            return
        warning = {}
        title = False
        message = False
        for r in self:
            self.num_id.ensayo = r.num_id.ensayo
            r.ensayo = r.num_id.ensayo
            r.product_id = r.production_id = False
            if r.num_id.ensayo == "celdas":
                e_obj = self.env["res.celdas"]
                cond = [("celda_num", "=", r.numserie)]
            elif r.num_id.ensayo == "fusibles":
                e_obj = self.env["res.fusibles"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.num_id.ensayo == "selas":
                e_obj = self.env["res.seccionadores"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.num_id.ensayo == "pararrayos":
                e_obj = self.env["res.pararrayos"]
                cond = [("num_serie", "=", r.numserie)]
            elif r.num_id.ensayo == "aisladores":
                e_obj = self.env["res.aisladores"]
                cond = [("num_serie", "=", r.numserie)]
            e_ids = e_obj.search(cond, limit=1)
            if e_ids:
                r.production_id = e_ids.production_id.id
                r.product_id = e_ids.product_id.id
                r.peso_sf6 = 0
                if r.num_id.ensayo == "celdas":
                    r.peso_sf6 = e_ids.peso_sf6
            else:
                r.numserie = False
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
                    f"{num_ids.venta_id.name} y producto "
                    f"{num_ids.product_id.default_code}"
                )
                warning["title"] = title
                warning["message"] = message
                r.numserie = False
                return {"warning": warning}
            lin_ids = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", r.num_id.venta_id.id),
                    ("product_id", "=", r.product_id.id),
                ],
                limit=1,
            )
            if lin_ids:
                r.linea_venta_id = lin_ids.id
                r.venta_id = lin_ids.order_id
            if not lin_ids:
                title = "Aviso"
                message = (
                    "El producto del número de serie no está en la OV "
                    f"{r.venta_id.name}"
                )
                warning["title"] = title
                warning["message"] = message
                r.numserie = False
                r.product_id = False
                return {"warning": warning}
        return {}
