from . import models


def _post_install_put_sale_lead_in_account_invoice(env):
    cond = [("opportunity_id", "!=", False)]
    sales = env["sale.order"].search(cond)
    for sale in sales:
        if sale.invoice_ids:
            sale.invoice_ids.write({"opportunity_id": sale.opportunity_id.id})
