import logging

from openupgradelib import openupgrade

from odoo import _

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cond = [("project_id", "!=", False)]
    sales = env["sale.order"].search(cond)
    for sale in sales:
        try:
            if sale.invoice_ids:
                for invoice in sale.invoice_ids.filtered(
                    lambda z: not z.account_analytic_id
                ):
                    invoice.write(
                        {
                            "account_analytic_id": sale.project_id.account_id.id,
                        }
                    )
        except Exception:
            _logger.error = _("Error processing sale order: %(sale_name)s.") % {
                "sale_name": sale.name,
            }
