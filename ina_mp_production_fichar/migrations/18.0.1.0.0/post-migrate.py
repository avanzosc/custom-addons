# Copyright 2026 Inael
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def _table_exists(cr, table_name):
    cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
        (table_name,),
    )
    return bool(cr.fetchone())


def _column_exists(cr, table_name, column_name):
    cr.execute(
        "SELECT 1 FROM information_schema.columns "
        "WHERE table_name = %s AND column_name = %s",
        (table_name, column_name),
    )
    return bool(cr.fetchone())


def _migrate_perfil(cr):
    """hr_employee_fichar -> columnas nuevas de hr_employee."""
    if not _table_exists(cr, "hr_employee_fichar"):
        _logger.info(
            "ina_mp_production_fichar: no existe hr_employee_fichar, nada "
            "que migrar del perfil."
        )
        return

    candidate_columns = [
        "tipo",
        "workorder_id",
        "repara_id",
        "laser_id",
        "improductivo",
        "puesto_id",
        "entrada_ultima",
        "salida_ultima",
    ]
    columns = [
        c
        for c in candidate_columns
        if _column_exists(cr, "hr_employee_fichar", c)
        and _column_exists(cr, "hr_employee", c)
    ]
    if not columns:
        _logger.warning(
            "ina_mp_production_fichar: hr_employee_fichar existe pero no "
            "hay columnas migrables en comun con hr_employee."
        )
        return

    # Los nombres de columna no se pueden pasar como parametro %s de
    # psycopg2 (eso solo vale para valores, no para identificadores). "columns"
    # sale de una lista blanca fija (candidate_columns) filtrada por
    # _column_exists, no de entrada de usuario, asi que es seguro.
    set_clause = ", ".join(f"{c} = hef.{c}" for c in columns)
    query = f"""
        UPDATE hr_employee he
        SET {set_clause}
        FROM hr_employee_fichar hef
        WHERE hef.employee_id = he.id
        """
    cr.execute(query)  # pylint: disable=sql-injection
    _logger.info(
        "ina_mp_production_fichar: %s empleados actualizados con su perfil "
        "de fichar antiguo (%s)",
        cr.rowcount,
        ", ".join(columns),
    )


def _migrate_historico(cr):
    """hr_fichar_historico.fichar_id (perfil) -> employee_id (empleado)."""
    if not _table_exists(cr, "hr_fichar_historico"):
        return
    if not _column_exists(cr, "hr_fichar_historico", "fichar_id"):
        _logger.info(
            "ina_mp_production_fichar: hr_fichar_historico ya no tiene "
            "fichar_id, nada que repuntar."
        )
        return
    if not _table_exists(cr, "hr_employee_fichar"):
        _logger.warning(
            "ina_mp_production_fichar: hr_fichar_historico.fichar_id existe "
            "pero hr_employee_fichar no. No se puede repuntar a "
            "employee_id automaticamente."
        )
        return

    cr.execute(
        """
        UPDATE hr_fichar_historico hfh
        SET employee_id = hef.employee_id
        FROM hr_employee_fichar hef
        WHERE hfh.fichar_id = hef.id
          AND hfh.employee_id IS NULL
        """
    )
    _logger.info(
        "ina_mp_production_fichar: %s lineas de historico repuntadas de "
        "fichar_id a employee_id",
        cr.rowcount,
    )


def migrate(cr, version):
    _migrate_perfil(cr)
    _migrate_historico(cr)
    _logger.info(
        "ina_mp_production_fichar: migracion %s completada. Las tablas/"
        "columnas antiguas no se borran aqui explicitamente; Odoo las "
        "limpiara solo al terminar de cargar los modulos.",
        version,
    )
