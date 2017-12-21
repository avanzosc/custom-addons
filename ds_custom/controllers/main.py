# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale
from openerp import SUPERUSER_ID


class WebsiteSale(website_sale):

    @http.route(['/shop/confirm_order'], type='http', auth="public",
                website=True)
    def confirm_order(self, **post):
        cr, context = (request.cr, request.context)
        super(WebsiteSale, self).confirm_order()
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.registry['sale.order'].browse(
                cr, SUPERUSER_ID, sale_order_id, context=context)
        else:
            return request.redirect('/shop')
        request.website.sale_reset(context=context)
        return request.website.render("website_sale.confirmation",
                                      {'order': order})
