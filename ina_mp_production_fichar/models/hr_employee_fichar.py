# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class HrEmployeeFichar(models.Model):
    _name = "hr.employee.fichar"
    _description = "Fichar Empleados Herencia de hr.employee"
    _rec_names_search = ["barcode", "name"]

    _sql_constraints = [
        (
            "employee_fichar_uniq",
            "UNIQUE(employee_id)",
            "Empleado debe de ser unico",
        ),
    ]

    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Empleado",
        required=True,
        ondelete="cascade",
        index=True,
    )
    barcode = fields.Char(
        string="Codigo",
        related="employee_id.barcode",
        store=True,
        groups="base.group_user",
    )
    name = fields.Char(string="Nombre", related="employee_id.name", store=True)
    fichar = fields.Selection(related="employee_id.fichar")
    entrada_ultima = fields.Datetime(string="Ultima Entrada")
    salida_ultima = fields.Datetime(string="Ultima Salida")
    tipo = fields.Selection(
        selection=[
            ("of", "En Fabricacion"),
            ("repara", "En Reparacion"),
            ("laser", "En Laser"),
            ("impro", "En Improductivo"),
            ("no", "No tienes Orden"),
        ],
        string="Orden Actual",
        default="no",
    )
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder", string="Orden de Trabajo"
    )
    repara_id = fields.Many2one(comodel_name="repair.order", string="Reparacion")
    laser_id = fields.Many2one(comodel_name="mrp.laser.cut.order", string="Laser")
    improductivo = fields.Many2one(
        comodel_name="mrp.workcenter.productivity.loss", string="Improduct."
    )
    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar", string="Puesto")
    ot_qty_aproducir = fields.Float(
        string="OT: Cant. a producir",
        digits=(9, 2),
        related="workorder_id.qty_production",
        help="Cantidad a producir en la OT",
    )
    ot_qty_comunicada = fields.Float(
        string="OT: Cant. Comunicada",
        digits=(9, 2),
        related="workorder_id.qty_producing",
        help="Cantidad comunicada sin procesar",
    )
    ot_qty_producida = fields.Float(
        string="OT: Cant. Producida",
        digits=(9, 2),
        related="workorder_id.qty_produced",
        help="Cantidad producidas y procesadas",
    )
    ot_product_id = fields.Many2one(
        string="OT: Producto", related="workorder_id.product_id"
    )
    la_qty_aproducir = fields.Float(
        string="Laser: Cant. a producir",
        digits=(9, 2),
        related="laser_id.material_qty",
        help="Cantidad a producir en la Orden",
    )
    la_qty_producida = fields.Float(
        string="Laser: Cant. Producida",
        digits=(9, 2),
        related="laser_id.produced_qty",
        help="Cantidad producidas y procesadas",
    )
    la_product_id = fields.Many2one(
        string="Laser: Producto", related="laser_id.raw_material_id"
    )
    plano = fields.Char()
    editar_orden = fields.Boolean(compute="_compute_editar_orden")
    line_ids = fields.One2many(
        comodel_name="hr.fichar.historico",
        inverse_name="fichar_id",
        string="Lineas Fichar",
        copy=False,
    )
    inspeccion_of = fields.Boolean(
        string="Inspeccionar OF", related="workorder_id.product_id.inspeccion_of"
    )

    @api.depends_context("uid")
    def _compute_editar_orden(self):
        editar_orden = self.env.user.has_group(
            "ina_mc_permisos.group_inael_fabrica_respon_fichar"
        )
        for fichar in self:
            fichar.editar_orden = editar_orden

    @api.depends("barcode", "name")
    def _compute_display_name(self):
        for fichar in self:
            fichar.display_name = " ".join(
                filter(None, [fichar.barcode, (fichar.name or "")[:40]])
            )

    def action_ver_a_consumir(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "ina_mp_production_fichar.action_hr_stock_move_fichar"
        )
        action["domain"] = [("workorder_id", "=", self.workorder_id.id)]
        return action

    def button_scrap(self):
        self.ensure_one()
        action = self.workorder_id.button_scrap()
        action["context"]["default_puesto_id"] = self.puesto_id.id
        return action
