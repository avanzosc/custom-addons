.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========
TRUKEBAI
========

- New "Is a Truke" check, and "Max trukes" in product.
- New Truke product created by xml, with check "Is a Truke" activated.
- Incoming picking lines editable on tree.
- New truke_amount field in stock move lines.
- Cost price visible in incoming stock move lines.
- Show and allow to edit cost price and truke amount values in transfer wizard.
- Allow to print product labels and a ticket in an incoming picking.
- Create a new outgoing picking when transferring incoming pickings.
  This outgoing picking will move the "Truke" product to the customer with
  the sum of all truke_amount fields in the incoming picking as outgoing
  quantity.
- In sale order, and in point of sale, new field "Contributed trukes". In sale
  order line, and lines of point of sale, new field "Max trukes" related to
  field "Max trukes" of the product. New button "Trukes management" in sale
  order, and in point of sale.
- When change "Contributed trukes". If the sum of "Max trukes" of her lines is
  > than "Contributed trukes". The value of the sum of "Max trukes" go to
  "Contridubited trukes" field. If the value of the field "Contributed trukes"
  is > than the sum of trukes of the client, the sum of trukes of the client
  go to "Contributed trukes".
- When confirm sale order, of the sale from the point of sale, and the field
  "Contributed trukes" > 0, a new line is given with this amount.


Credits
=======

Contributors
------------
* Ainara Galdona <ainaragaldona@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
