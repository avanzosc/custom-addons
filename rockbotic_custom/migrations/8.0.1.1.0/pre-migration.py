# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def delete_view(cr):
    cr.execute(
        """
        DELETE FROM ir_ui_view WHERE id IN
            (SELECT res_id
               FROM ir_model_data
              WHERE module = 'rockbotic_custom'
                AND name = 'rockbotic_event'
                AND model = 'ir.ui.view');
        """)
    cr.execute(
        """
        DELETE FROM ir_model_data
          WHERE module = 'rockbotic_custom'
            AND name = 'rockbotic_event'
            AND model = 'ir.ui.view';
        """)


def migrate(cr, version):
    if not version:
        return
    delete_view(cr)
