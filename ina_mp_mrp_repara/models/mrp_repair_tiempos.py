# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MrpRepairTiempos(models.Model):
    _name = "mrp.repair.tiempos"
    _description = "Tiempos en Reparaciones"

    @api.depends("entrada", "salida")
    def _compute_tiempo(self):
        for r in self:
            if r.entrada and r.salida:
                delta = r.salida - r.entrada
                r.tiempo = delta.total_seconds() / 3600.0
            else:
                r.tiempo = 0.0

    repara_id = fields.Many2one(
        comodel_name="repair.order",
        string="Orden Reparacion",
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter",
        string="Centro de Produccion",
        related="repara_id.workcenter_id",
        store=True,
    )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")
    entrada = fields.Datetime(string="Inicio")
    salida = fields.Datetime(string="Final")
    tiempo = fields.Float(
        string="Duracion HH:MM",
        compute="_compute_tiempo",
        digits=(12, 6),
        store=True,
    )
    estado = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("cerrada", "Cerrada"),
            ("cancelada", "Cancelada"),
            ("interrumpida", "Interrumpida"),
            ("activa", "Activa"),
        ],
        default="pendiente",
        required=True,
    )
