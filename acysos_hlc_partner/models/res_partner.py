# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class PartnerSegment(models.Model):
    _name = "partner.segment"
    _description = "Partner Segment"

    name = fields.Char(required=True)


class ResPartner(models.Model):
    _inherit = "res.partner"

    ext_id = fields.Char(string="External id")
    hlc_segment_id = fields.Many2one(
        comodel_name="partner.segment",
        string="Segment",
    )
