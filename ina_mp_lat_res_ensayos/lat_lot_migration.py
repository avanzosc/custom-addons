# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import SUPERUSER_ID
from odoo.tools import SQL

_logger = logging.getLogger(__name__)


def _column_type(cr, table, column):
    cr.execute(
        "SELECT data_type FROM information_schema.columns"
        " WHERE table_name = %s AND column_name = %s",
        [table, column],
    )
    return cr.fetchone()[0]


def _serial_sql(cr, table, column):
    col = SQL.identifier("r", column)
    column_type = _column_type(cr, table, column)
    if column_type == "numeric":
        return SQL("NULLIF(TRIM_SCALE(%s), 0)::varchar", col)
    if column_type == "integer":
        return SQL("NULLIF(%s, 0)::varchar", col)
    return SQL("NULLIF(TRIM(%s), '')", col)


def serial_to_lot(cr, table, column, product_column="product_id"):
    params = {
        "table": SQL.identifier(table),
        "serial": _serial_sql(cr, table, column),
        "product": SQL.identifier("r", product_column),
        "uid": SUPERUSER_ID,
        "now": cr.now(),
    }
    cr.execute(
        SQL(
            """
            INSERT INTO stock_lot (
                name, product_id, product_uom_id, company_id,
                create_uid, create_date, write_uid, write_date)
            SELECT src.name, src.product_id, pt.uom_id, pt.company_id,
                   %(uid)s, %(now)s, %(uid)s, %(now)s
              FROM (SELECT DISTINCT %(product)s AS product_id, %(serial)s AS name
                      FROM %(table)s r
                     WHERE %(product)s IS NOT NULL) src
              JOIN product_product pp ON pp.id = src.product_id
              JOIN product_template pt ON pt.id = pp.product_tmpl_id
             WHERE src.name IS NOT NULL
               AND NOT EXISTS (
                   SELECT 1 FROM stock_lot l
                    WHERE l.product_id = src.product_id AND l.name = src.name)
            RETURNING product_id
            """,
            **params,
        )
    )
    created = cr.rowcount
    product_ids = {product_id for (product_id,) in cr.fetchall()}
    cr.execute(
        SQL(
            """
            UPDATE %(table)s r SET lot_id = l.id
              FROM stock_lot l
             WHERE r.lot_id IS NULL
               AND l.product_id = %(product)s
               AND l.name = %(serial)s
            """,
            **params,
        )
    )
    _logger.info(
        "%s: %s lotes creados, %s registros con numero de serie",
        table,
        created,
        cr.rowcount,
    )
    return product_ids


def clear_converted(cr, table, column):
    cr.execute(
        SQL(
            "UPDATE %s SET %s = NULL WHERE lot_id IS NOT NULL",
            SQL.identifier(table),
            SQL.identifier(column),
        )
    )


def keep_serial_in_name(cr, table, column):
    if _column_type(cr, table, "name") != _column_type(cr, table, column):
        return
    query = SQL(
        "UPDATE %(table)s SET name = %(col)s WHERE lot_id IS NULL"
        " AND %(col)s IS NOT NULL AND name IS DISTINCT FROM %(col)s",
        table=SQL.identifier(table),
        col=SQL.identifier(column),
    )
    cr.execute(query)
    if cr.rowcount:
        _logger.info(
            "%s: numero de serie copiado a name en %s filas", table, cr.rowcount
        )


def rename_in_filters(cr, model, old_field, new_field):
    cr.execute(
        """
        UPDATE ir_filters
           SET domain = regexp_replace(domain, %(old)s, %(new)s, 'g'),
               context = regexp_replace(context, %(old)s, %(new)s, 'g'),
               sort = regexp_replace(sort, %(old)s, %(new)s, 'g')
         WHERE model_id = %(model)s
        """,
        {
            "old": f"(['\"]){old_field}(['\"])",
            "new": rf"\1{new_field}\2",
            "model": model,
        },
    )


def set_tracking(env, product_ids, tracking="serial"):
    replaceable = ("none", "lot") if tracking == "serial" else ("none",)
    templates = (
        env["product.product"]
        .with_context(active_test=False)
        .browse(product_ids)
        .product_tmpl_id.filtered(lambda t: t.is_storable and t.tracking in replaceable)
    )
    templates.write({"tracking": tracking})
    _logger.info("Seguimiento '%s' en %s productos", tracking, len(templates))
