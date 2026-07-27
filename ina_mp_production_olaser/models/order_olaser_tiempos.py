# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class OrderOlaserTiempos(models.Model):
    _name = "order.olaser.tiempos"
    _description = "Tiempos en O.Laser"

    @api.depends("entrada", "salida")
    def _compute_tiempo(self):
        if self.entrada and self.salida:
            timedelta = fields.Datetime.from_string(
                self.salida
            ) - fields.Datetime.from_string(self.entrada)
            self.tiempo = timedelta.total_seconds() / 3600.0

    laser_tiempos_id = fields.Many2one(
        comodel_name="order.olaser", string="Orden Laser"
    )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")
    entrada = fields.Datetime(string="Inicio")
    salida = fields.Datetime(string="Final")
    tiempo = fields.Float(
        string="Duracion HH:MM", compute="_compute_tiempo", digits=(12, 6), store=True
    )
    estado = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("cerrada", "Cerrada"),
            ("cancelada", "Cancelada"),
            ("interrumpida", "Interrumpida"),
            ("activa", "Activa"),
        ],
        default="pendiente",
        required=True,
    )
    comunicado = fields.Float(string="Qt. Comunicada", digits=(9, 2), default=0)
