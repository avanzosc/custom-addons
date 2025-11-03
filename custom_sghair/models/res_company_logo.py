# Copyright 2019 Alfredo de la Fuente - Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResCompanyLogo(models.Model):
    _name = "res.company.logo"
    _description = "Company logos"

    name = fields.Char(string="Description", required=True, copy=False)
    logo = fields.Binary(required=True, copy=False)
    use_default = fields.Boolean(
        string="Use this for default", default=False, copy=False
    )

    def get_default_logo(self):
        cond = [("use_default", "=", True)]
        logo = self.search(cond, limit=1)
        a = logo if logo else self.env["res.company.logo"]
        return a
