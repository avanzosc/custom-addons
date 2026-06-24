# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64

from odoo import http
from odoo.http import request


class DirectDownloadController(http.Controller):
    @http.route("/my/direct/download_pdf", type="http", auth="user")
    def download_pdf(self, **kwargs):
        file_name = kwargs.get("fname", "documento")
        key = f"ver_pdf_{request.env.user.id}"
        pdf_b64 = request.env["ir.config_parameter"].sudo().get_param(key)
        if not pdf_b64:
            return request.not_found()
        pdf = base64.b64decode(pdf_b64)
        filename = f"{file_name}"
        return request.make_response(
            pdf,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Disposition", f'attachment; filename="{filename}"'),
            ],
        )
