# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpImproductivo(models.Model):
    _name = "mrp.improductivo"
    _description = "Tiempos Improductivos"
    _order = "entrada DESC"

    # --- Logica operativa comentada: solo referencia, no se ejecuta. ---

    # @api.depends("entrada", "salida")
    # def _compute_tiempo(self):
    #     for r in self:
    #         if r.entrada and r.salida:
    #             delta = r.salida - r.entrada
    #             r.tiempo = delta.total_seconds() / 3600.0
    #         else:
    #             r.tiempo = 0.0

    loss_id = fields.Many2one(
        comodel_name="mrp.workcenter.productivity.loss",
        string="Tipo Improductivo",
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter", string="Centro de Produccion"
    )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")
    entrada = fields.Datetime(string="Inicio")
    salida = fields.Datetime(string="Final")
    tiempo = fields.Float(
        string="Duracion HH:MM",
        digits=(12, 6),
    )
    # Definicion real: compute="_compute_tiempo", store=True (ver metodo
    # comentado mas arriba).
    estado = fields.Selection(
        selection=[
            ("pendiente", "Pendiente"),
            ("activa", "Activa"),
            ("interrumpida", "Interrumpida"),
            ("cerrada", "Cerrada"),
            ("cancelada", "Cancelada"),
        ],
        default="pendiente",
        required=True,
    )
