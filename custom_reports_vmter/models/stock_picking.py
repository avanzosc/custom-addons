# 2018 Alquemy - Javier de las Heras <jheras@alquemy.es>
# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_format_date_by_lang(self, date):
        self.ensure_one()
        lang_domain = [("code", "=", self.env.lang)]
        lang = self.env["res.lang"].search(lang_domain, limit=1)
        d_format = lang.date_format if lang else "%m/%d/%Y"
        return fields.Date.from_string(date).strftime(d_format)

    def _get_format_float_by_lang(self, float_format):
        self.ensure_one()
        lang_domain = [("code", "=", self.env.lang)]
        lang = self.env["res.lang"].search(lang_domain, limit=1)
        res = "{:3,.2f}".format(float_format)
        if lang:
            res = res.replace(",", "COMMA")
            res = res.replace(".", "DOT")
            res = res.replace("COMMA", lang.thousands_sep)
            res = res.replace("DOT", lang.decimal_point)
        return res

    def _get_lots(self, move):
        res = {}
        for line_id in move.move_line_ids:
            if line_id.lot_id:
                if not res.get(line_id.lot_id.name):
                    if line_id.lot_id.expiration_date:
                        date_row = line_id.lot_id.expiration_date
                        date_type = "expiration_date"
                        formatted_date = self._get_format_date_by_lang(
                            line_id.lot_id.expiration_date)
                    elif line_id.lot_id.use_date:
                        date_row = line_id.lot_id.use_date
                        date_type = "use_date"
                        formatted_date = self._get_format_date_by_lang(
                            line_id.lot_id.use_date)
                    else:
                        date_row = ""
                        date_type = False
                        formatted_date = False
                    formatted_qty = self._get_format_float_by_lang(
                        line_id.qty_done)
                    lot_data = {"date": formatted_date,
                                "date_row": date_row,
                                "date_type": date_type,
                                "name": line_id.lot_id.name,
                                "qty": line_id.qty_done,
                                "qty_formatted": formatted_qty,
                                "uom": self.product_uom.name}
                    res[line_id.lot_id.name] = lot_data
                else:
                    res[line_id.lot_id.name]["qty"] += line_id.qty_done
                    formatted_qty = self._get_format_float_by_lang(
                        res[line_id.lot_id.name]["qty"])
                    res[line_id.lot_id.name]["qty_formatted"] = formatted_qty
        result = [x for x in res.values()]
        result = sorted(result, key=lambda x: x["name"])
        result = sorted(result, key=lambda x: x["date_row"])
        return result
