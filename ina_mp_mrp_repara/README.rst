.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://opensource.org/licenses/AGPL-3.0
   :alt: License: AGPL-3

=================
Ina MP MRP Repara
=================

Gestión de Reparaciones.

Extiende el módulo ``repair`` de Odoo con:

- Estado intermedio *Pendiente Confirmacion* (``pteconfir``) en el flujo de reparaciones.
- Campos de clasificación: Tipo de Reparación, Motivo, Centro de Producción, OF vinculada.
- Creación de materiales de reparación a partir de los materiales definidos en el producto.
- Coste de la línea de reparación desde el precio estándar del producto.
- Bloqueo de productos fantasma como materiales en reparaciones.
- Registro de tiempos por empleado (``mrp.repair.tiempos``).
- Gestión de documentación adjunta desde el servidor de ficheros (``mrp.repair.docu``).

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/custom-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Inael
* Ana Juaristi <anajuaristi@avanzosc.es>
* Lucía Echeverría <luciaecheverria@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
