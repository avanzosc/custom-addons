.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=========================
Ina MP Production Fichar
=========================

Gestión de fichajes de fábrica: entrada/salida de empleados e imputación de
su tiempo y cantidades producidas a órdenes de fabricación, reparaciones,
trabajos de láser o tiempo improductivo.

El fichaje real de presencia se apoya en el modelo core ``hr.attendance`` en
lugar de un modelo propio de presencia.

Cómo funciona
==============

Modelos
-------

* ``hr.employee`` (extendido): hace de "perfil" de fichaje — una fila fija
  por empleado con su orden actual (``tipo``, y según el tipo
  ``workorder_id``, ``repara_id``, ``laser_id`` o ``improductivo``), su
  puesto y su estado de presencia (``proximo_movi``: si le toca fichar
  entrada o salida).
* ``hr.attendance`` (core, sin campos añadidos por este módulo): el log real
  de entradas y salidas. Cada fichaje de "Entrada - Salida" crea o cierra un
  registro aquí.
* ``hr.puesto.fichar``: un puesto de trabajo físico (centro de trabajo,
  ubicación de consumo, ubicación de desechos) asociado a un usuario de
  Odoo. Pensado para que cada terminal/ordenador de fábrica tenga su propio
  usuario fijo, de forma que el sistema sepa en qué puesto está sin
  preguntar.
* ``hr.fichar.historico``: histórico de líneas de trabajo por empleado (tipo
  de orden, fechas, cantidades aceptadas/rechazadas, puesto), de solo
  consulta.
* ``wiz.fichar.orden``: wizard que se abre al fichar entrada sin ninguna
  orden activa, o al pulsar "Nueva Orden" / "Comunicar Cantidad".

Flujo de fichaje
-----------------

1. El empleado ficha **Entrada - Salida** desde el tablero del mismo nombre
   (una fila por empleado).
2. Si no tiene ninguna orden activa y ficha en modo "Fabrica", se abre
   automáticamente el wizard **Fichar Orden**: ahí elige en qué va a
   trabajar (Fabricación, Reparación, Láser o Improductivo) y en qué
   **Puesto** está (por defecto se sugiere el del usuario de Odoo actual,
   pero se puede cambiar cada vez).
3. Al confirmar ("Crear Orden") se abre un registro de tiempo — según el
   tipo, en ``mrp.workcenter.productivity``, ``mrp.repair.tiempos``,
   ``order.olaser.tiempos`` o ``mrp.improductivo`` — y una línea nueva en el
   histórico.
4. Mientras trabaja, puede pulsar **Comunicar Cantidad** para informar de
   piezas aceptadas/rechazadas sin dejar la orden: cierra el tramo de
   tiempo/histórico actual y abre uno nuevo para seguir imputando en la
   misma orden.
5. **Parar Orden** cierra el tiempo/histórico actual sin comunicar ninguna
   cantidad y deja al empleado sin orden asignada, reabriendo el wizard para
   que elija la siguiente tarea.
6. Al fichar salida se cierra la asistencia (``hr.attendance``) y, si tenía
   una orden activa, ésta queda marcada como interrumpida (sin comunicar
   cantidad).

Finalizar formalmente una orden de trabajo (dejarla en estado "Hecho") se
sigue haciendo desde la pantalla nativa de Fabricación de Odoo, no desde
este módulo — el fichaje solo imputa tiempo y cantidades parciales.

Menús (Fichar)
---------------

* **Entrada - Salida**: tablero de fichaje, una fila por empleado con su
  estado actual.
* **Alta en Fichajes**: lista editable para asignar el código de barras a
  los empleados que fichan.
* **Puesto para Fichar**: alta y configuración de los puestos de trabajo
  físicos.

Otras acciones desde la ficha de fichaje
-------------------------------------------

* **Desechos**: abre el formulario de scrap con la orden y el puesto ya
  precargados.
* **Material de la Orden**: lista del material a consumir de la orden de
  fabricación activa, con acceso rápido a existencias.
* **Histórico**: pestaña con todas las líneas de trabajo del empleado. Se
  pueden borrar si hay un error al comunicar una cantidad — al borrar, se
  revierte automáticamente lo que esa línea había sumado a la orden de
  trabajo.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/custom-addons/issues>`_.

Credits
=======

Contributors
------------

* INAEL, jag
* Ana Juaristi <ajuaristio@gmail.com>
* Lucía Echeverría <luciaecheverria@avanzosc.es>
