# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrFicharHistorico(models.Model):
    _name = "hr.fichar.historico"
    _description = "Historico de fichajes"
    _order = "id DESC"

    fichar_id = fields.Many2one(
        comodel_name="hr.employee.fichar",
        string="Empleado",
        ondelete="cascade",
        index=True,
    )
    tipo = fields.Selection(
        selection=[
            ("of", "Fabricacion"),
            ("repara", "Reparacion"),
            ("laser", "Laser"),
            ("impro", "Improductivo"),
            ("no", ""),
        ],
        string="Fichado en",
        default="no",
    )
    orden = fields.Char()
    fecha_ini = fields.Datetime(string="Inicio")
    fecha_fin = fields.Datetime(string="Final")
    aceptada = fields.Float(string="Cantidad Aceptada")
    rechazada = fields.Float(string="Cantidad Rechazada")
    puesto_id = fields.Many2one(comodel_name="hr.puesto.fichar", string="Puesto")
    estado = fields.Char()
