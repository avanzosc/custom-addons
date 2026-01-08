# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    cancelled_quotation_count = fields.Integer(
        string="Cancelled quotations", compute="_compute_count_cancelled_quotations"
    )
    lead_type_id = fields.Many2one(
        string="Lead Type", comodel_name="type", index=True, ondelete="restrict"
    )
    brand_id = fields.Many2one(
        string="Brand", comodel_name="brand", index=True, ondelete="restrict"
    )
    belong_id = fields.Many2one(
        string="It belongs to", comodel_name="belongs", index=True, ondelete="restrict"
    )

    @api.depends("order_ids.state")
    def _compute_count_cancelled_quotations(self):
        for lead in self:
            lead.cancelled_quotation_count = 0
            for order in lead.order_ids:
                if order.state == "cancel":
                    lead.cancelled_quotation_count += 1

    def action_view_sale_cancelled_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale.action_quotations_with_onboarding"
        )
        action["context"] = {
            "default_partner_id": self.partner_id.id,
            "default_opportunity_id": self.id,
        }
        action["domain"] = [("opportunity_id", "=", self.id), ("state", "=", "cancel")]
        quotations = self.mapped("order_ids").filtered(lambda x: x.state in ("cancel"))
        if len(quotations) == 1:
            action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
            action["res_id"] = quotations.id
        return action
