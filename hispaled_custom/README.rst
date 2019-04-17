.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

========================
HISPALED - Custom module
========================

This module customizes Odoo for HISPALED:

* Adds two fields to manufacturing orders:
   * IP Safeguard
   * IK Safeguard

* Adds 'sum' in the tree view of the produced products to watch total quantity
* Appliance classes defined symbol, attribute code must be LUM-CLA and names are:
   * ClassI name: 'I'
   * ClassII name: 'II'
   * ClassIII name: 'III'

* Customized purchase order, sale order, invoice and stock picking reports.
* Propagate sale order to out picking, and out invoices.
* Catch the description of the variants of the products for sales, purchases,
  pickings, and invoices lines.

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

* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>

Do not contact contributors directly about support or help with technical issues.
