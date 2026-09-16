from werkzeug.utils import redirect

from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.website.controllers.main import QueryURL


class PortalStock(CustomerPortal):
    def _redirect_to_portal_catalog(self, path):
        query_string = request.httprequest.query_string.decode()
        url = path
        if query_string:
            url = f"{url}?{query_string}"
        return request.redirect(url)

    @http.route(
        ["/odoo/my/catalog", "/odoo/my/catalog/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def portal_my_catalogs_backend_redirect(self, page=1, **kw):
        path = "/my/catalog"
        if page != 1:
            path = f"/my/catalog/page/{page}"
        return self._redirect_to_portal_catalog(path)

    @http.route(
        [
            "/odoo/my/catalog/<int:catalog_id>",
            "/odoo/my/catalog/<int:catalog_id>/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def portal_my_catalog_backend_redirect(self, catalog_id=None, page=1, **kw):
        path = f"/my/catalog/{catalog_id}"
        if page != 1:
            path = f"{path}/page/{page}"
        return self._redirect_to_portal_catalog(path)

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        Catalog = request.env["product.catalog.web"]
        domain = [("active", "=", True), ("visible_slider", "=", True)]
        catalogs = Catalog.search(domain)
        values.update(
            {
                "catalog_ids": catalogs,
                "catalog_count": len(catalogs),
            }
        )
        return values

    def filter_catalog_data(self, args, catalog_filters=None):
        domain = []

        if (
            "filterby" in args
            and args.get("filterby") not in ["all", ""]
            and catalog_filters
        ):
            domain += catalog_filters[args.get("filterby")]["domain"]

        if "brand" in args and args.get("brand") not in ["all", ""]:
            domain += [("product_brand_id", "=", int(args.get("brand")))]

        if "search" in args and args.get("search") != "":
            search = args.get("search")
            domain += [
                "|",
                ("name", "ilike", search),
                "|",
                ("product_brand_id.name", "ilike", search),
                "|",
                ("default_code", "ilike", search),
                ("barcode", "ilike", search),
            ]

        return domain

    @http.route(
        ["/my/catalog", "/my/catalog/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def portal_my_catalogs(
        self,
        catalog_id=None,
        page=1,
        access_token=None,
        report_type=None,
        catalog_download=None,
        download=False,
        **kw,
    ):
        # Prepare values
        values = self._prepare_portal_layout_values()
        catalog_model = request.env["product.catalog.web"]
        domain = [("active", "=", True), ("visible_slider", "=", True)]
        catalog_count = values.get("catalog_count")
        default_url = "/my/catalog"

        if report_type == "xlsx" and download and catalog_download:
            catalog = catalog_model.browse(int(catalog_download))
            order = request.website.sale_get_order()
            attachment_id = False
            if "btn_download" in kw:
                attachment_id, file_name = catalog.create_excel_file(sale_order=order)
            if "btn_extended" in kw:
                logged_user = request.env.user.sudo()
                attachment_id, file_name = catalog.create_excel_file_extended(
                    order.partner_id or logged_user.partner_id, catalog
                )
            if attachment_id:
                return redirect(
                    "/web/content/?model=ir.attachment&field=datas&download"
                    f"=true&id={attachment_id}&filename={file_name}"
                )

        pager = portal_pager(
            url="/my/catalog", total=catalog_count, page=page, step=self._items_per_page
        )
        catalogs = catalog_model.search(
            domain, limit=self._items_per_page, offset=pager["offset"]
        )

        keep = QueryURL(
            "/my/catalog",
            report_type=report_type,
            catalog_download=catalog_download,
            download=download,
        )

        values.update(
            {
                "page_name": "catalog",
                "pager": pager,
                "default_url": default_url,
                "catalog_ids": catalogs,
                "keep": keep,
            }
        )
        return request.render("website_portal_catalog.portal_my_catalog", values)

    @http.route(
        [
            "/my/catalog/<int:catalog_id>",
            "/my/catalog/<int:catalog_id>/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def portal_my_catalog(
        self,
        catalog_id=None,
        page=1,
        sortby=None,
        search_in="all",
        access_token=None,
        report_type=None,
        download=False,
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        Product = request.env["product.template"]
        Catalog = request.env["product.catalog.web"]
        catalog = Catalog.sudo().browse(catalog_id)

        if report_type == "xlsx" and download:
            order = request.website.sale_get_order()
            attachment_id, file_name = catalog.create_excel_file(sale_order=order)
            return redirect(
                "web/content/?model=ir.attachment&field=datas&download"
                f"=true&id={attachment_id}&filename={file_name}"
            )

        keep = QueryURL(
            f"/my/catalog/{catalog_id}", report_type=report_type, download=download
        )

        domain = [("id", "in", catalog.product_ids.ids), ("is_published", "=", True)]

        user_id = request.env.user
        pricelist = user_id.partner_id.property_product_pricelist
        if user_id.is_commercial != "all":
            domain += [("id", "in", pricelist.product_ids.ids)]

        all_products = Product.sudo().search(domain)
        product_brand_ids = (
            all_products.mapped("product_brand_id")
            if all_products
            else request.env["product.brand"]
        )
        searchbar_filters = self.get_catalog_filters(product_brand_ids)

        searchbar_inputs = {
            "all": {"input": "all", "label": _("Search in All")},
        }

        searchbar_sortings = {
            "category": {"label": _("Category"), "order": "categ_id"},
            "name": {"label": _("Name"), "order": "name"},
            "brand": {"label": _("Brand"), "order": "product_brand_id"},
            "price": {"label": _("Price"), "order": "list_price"},
        }

        # default sortby order
        if not sortby:
            sortby = "category"
        sort_order = searchbar_sortings[sortby]["order"]
        filterby = kw.get("filterby") if "filterby" in kw else "all"
        brand = kw.get("brand") if "brand" in kw else "all"

        search = kw.get("search")
        domain += self.filter_catalog_data(kw, searchbar_filters)
        filtered_products = Product.sudo().search(domain)
        product_count = len(filtered_products)
        default_url = "/my/catalog/" + str(catalog_id)
        pager = portal_pager(
            url=default_url,
            url_args={
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
                "filterby": filterby,
                "brand": brand,
            },
            total=product_count,
            page=page,
            step=self._items_per_page,
        )
        products = Product.sudo().search(
            domain, order=sort_order, limit=self._items_per_page, offset=pager["offset"]
        )

        values.update(
            {
                "pager": pager,
                "page_name": "catalog",
                "default_url": default_url,
                "pricelist": pricelist,
                "catalog": catalog,
                "products": products,
                # 'brand': brand,
                # 'product_brand_ids': product_brand_ids,
                "keep": keep,
                "sortby": sortby,
                "filterby": filterby,
                "search": search,
                "search_in": search_in,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "searchbar_filters": searchbar_filters,
            }
        )
        return request.render("website_portal_catalog.portal_catalog", values)

    def get_catalog_filters(self, brands):
        searchbar_filters = {
            "all": {"label": _("All Brands"), "domain": []},
        }

        for brand in brands:
            searchbar_filters.update(
                {
                    str(brand.id): {
                        "label": _(brand.name),
                        "domain": [("product_brand_id.id", "=", brand.id)],
                    }
                }
            )

        return searchbar_filters
