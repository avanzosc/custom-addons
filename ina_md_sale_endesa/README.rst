.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=======================
Entegas de OV de Endesa
=======================

* Menu «Ventas > Pedidos > Entregas Endesa» con el seguimiento de las lineas
  de pedido de venta de Endesa: cantidad pedida y entregada, destino,
  contrato, fecha planificada, fecha de necesidad, N/S, estado, ID, OF y
  si se ha enviado.
* La fecha de necesidad se colorea segun lo cerca que este: rojo si ya ha
  vencido, naranja si faltan 7 dias o menos y amarillo si faltan 15 dias o
  menos (salvo en estado QA).
* La fecha de fabricacion es la fecha planificada menos 7 dias.
* Boton «Actualizar Entregas» en el listado: añade las lineas de los
  pedidos confirmados desde 2025 de los clientes de Endesa con productos
  homologados por Enel que aun no estan en el listado, y recalcula los
  colores.
* Campo «Fecha Planificada» en el pedido de venta.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/custom-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Contributors
------------
* Inael
* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
