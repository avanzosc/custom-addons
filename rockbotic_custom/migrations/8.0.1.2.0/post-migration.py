# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def assign_download_filename(cr):
    cr.execute(
        """
            UPDATE ir_act_report_xml
            SET download_filename = '${o.number}.pdf'
            WHERE model = 'account.invoice';
        """)
    cr.execute(
        """
            UPDATE ir_act_report_xml
            SET download_filename = '${o.name}.pdf'
            WHERE model = 'sale.order';
        """)


def migrate(cr, version):
    if not version:
        return
    assign_download_filename(cr)
