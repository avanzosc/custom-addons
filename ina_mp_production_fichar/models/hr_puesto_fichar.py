# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class HrPuestoFichar(models.Model):
    _name = "hr.puesto.fichar"
    _description = "Puestos para fichar"

    name = fields.Char(required=True)
    user_id = fields.Many2one(
        comodel_name="res.users", string="Usuario Odoo", required=True
    )
    centro_id = fields.Many2one(
        comodel_name="mrp.workcenter", string="Centro asociado", required=True
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Ubicacion",
        domain="[('usage', '=', 'internal')]",
        required=True,
    )
    scrap_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Ubicacion Deshechos",
        domain="[('scrap_location', '=', True)]",
        required=True,
    )
