# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RepairOrder(models.Model):
    _inherit = "repair.order"

    @api.depends(
        "product_id", "product_id.product_tmpl_id.product_reparacion_ids", "move_ids"
    )
    def _compute_operacion_creada(self):
        for repair in self:
            material_lines = repair._get_materiales_reparacion()
            add_moves = repair.move_ids.filtered(
                lambda move: move.repair_line_type == "add"
            )
            repair.operacion_creada = not material_lines or bool(add_moves)

    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter", string="Centro de Produccion"
    )
    descripcion = fields.Text()
    repara_id = fields.One2many(
        comodel_name="mrp.repair.tiempos",
        inverse_name="repara_id",
        string="Tiempos Reparacion",
    )
    tipo_repara = fields.Selection(
        selection=[
            ("interna", "Interna Reprocesos Fabrica"),
            ("internaespecial", "Interna Trabajos Especiales"),
            ("internaotros", "Interna Otros Dptos."),
            ("externa", "Externa"),
            ("mto", "Mantenimiento"),
            ("abono", "Abono"),
        ],
        string="Tipo de Reparacion",
    )
    motivo_repara = fields.Selection(
        selection=[
            ("cali", "Calidad"),
            ("come", "Comercial"),
            ("comp", "Compras"),
            ("celd", "Fab/Celdas"),
            ("lase", "Fab/Laser"),
            ("enla", "Fab/Enlaces"),
            ("nobl", "Fab/Noblejas"),
            ("pren", "Fab/Prensas"),
            ("resi", "Fab/Resina"),
            ("trafo", "Fab/Trafos"),
            ("tecn", "Of. Tecnica"),
            ("gara", "Rep. en Garantia"),
            ("fuer", "Rep. fuera Garantia"),
            ("inve", "Sacar Inventario"),
            ("stoc", "Stock Incorrecto"),
            ("plan", "Planif. Fabrica"),
            ("alma", "Almacen"),
            ("labo", "Laboratorio"),
            ("dire", "Direccion"),
        ],
        string="Motivo",
    )
    line_documen_ids = fields.One2many(
        comodel_name="mrp.repair.docu",
        inverse_name="rma_id",
        string="Documentos",
        copy=True,
    )
    state = fields.Selection(
        selection_add=[("pteconfir", "Pendiente Confirmacion")],
        ondelete={"pteconfir": "set draft"},
    )
    operacion_creada = fields.Boolean(
        string="Operaciones Creadas",
        compute="_compute_operacion_creada",
    )

    def action_pte_confir(self):
        if self.filtered(lambda r: r.state != "draft"):
            raise UserError(
                _("Solo se puede poner Pte. confirmar cuando este en estado Borrador.")
            )
        return self.write({"state": "pteconfir"})

    def action_validate(self):
        self.ensure_one()
        if self.state != "pteconfir":
            raise UserError(_("Solo puede confirmar estando en Pte. Confirmar"))
        return super().action_validate()

    def action_repair_start(self):
        if self.filtered(lambda repair: repair.state != "confirmed"):
            raise UserError(_("Solo se puede iniciar una reparación confirmada."))
        return super().action_repair_start()

    def _action_repair_confirm(self):
        repairs_pteconfir = self.filtered(lambda r: r.state == "pteconfir")
        remaining = self - repairs_pteconfir
        if repairs_pteconfir:
            repairs_pteconfir._check_company()
            repairs_pteconfir.move_ids._check_company()
            repairs_pteconfir.move_ids._adjust_procure_method(
                picking_type_code="repair_operation"
            )
            repairs_pteconfir.move_ids._action_confirm()
            repairs_pteconfir.move_ids._trigger_scheduler()
            repairs_pteconfir.write({"state": "confirmed"})
        if remaining:
            return super()._action_repair_confirm()
        return True

    def _get_materiales_reparacion(self):
        self.ensure_one()
        if not self.product_id:
            return self.env["product.reparacion"]
        return self.product_id.product_tmpl_id.product_reparacion_ids.filtered(
            lambda line: line.material_id and line.cantidad
        )

    def action_crear_materiales(self):
        Move = self.env["stock.move"]
        for repair in self:
            material_lines = repair._get_materiales_reparacion()
            if not material_lines:
                raise UserError(
                    _(
                        "El producto de la reparación no tiene materiales de"
                        " reparación definidos."
                    )
                )
            if repair.move_ids.filtered(lambda move: move.repair_line_type == "add"):
                raise UserError(_("La reparación ya tiene materiales creados."))

            vals_list = []
            repair_qty = repair.product_qty or 1.0
            for line in material_lines:
                material = line.material_id
                vals_list.append(
                    {
                        "repair_id": repair.id,
                        "repair_line_type": "add",
                        "product_id": material.id,
                        "product_uom_qty": line.cantidad * repair_qty,
                        "product_uom": material.uom_id.id,
                        "price_unit": material.standard_price,
                        "company_id": repair.company_id.id,
                        "date": repair.schedule_date,
                        "location_id": repair.location_id.id,
                        "location_dest_id": repair.location_dest_id.id,
                    }
                )
            Move.create(vals_list)
        return True
