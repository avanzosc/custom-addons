from odoo import api, fields, models
from odoo.models import expression


class InternalProductCategory(models.Model):
    _name = "internal.product.category"
    _description = "Internal Product Category"

    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "internal_category_name_unique",
            "unique(name)",
            "Internal product category name must be unique.",
        )
    ]


class ProductSeries(models.Model):
    _name = "product.series"
    _description = "Product Series"

    name = fields.Char(required=True, index=True)

    _sql_constraints = [
        (
            "series_name_unique",
            "unique(name)",
            "Product series name must be unique.",
        )
    ]


class ProductSeason(models.Model):
    _name = "product.season"
    _description = "Product Season"

    name = fields.Char(required=True)


class ProductProduct(models.Model):
    _inherit = "product.product"

    b2b_virtual_available = fields.Float(
        string="B2B Quantity",
        compute="_compute_b2b_quantities",
        digits="Product Unit of Measure",
        compute_sudo=True,
    )

    def _compute_b2b_quantities(self):
        locations = self.env["stock.location"].search([("for_stock_b2b", "=", True)])
        for product in self:
            quantity = 0.0
            for location in locations:
                quantity += (
                    product.with_context(location=location.id).qty_available
                    - product.with_context(
                        location=location.id, only_for_b2b=True
                    ).outgoing_qty
                )
            product.b2b_virtual_available = quantity

    def _get_domain_locations(self):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = (
            super()._get_domain_locations()
        )
        if self.env.context.get("only_for_b2b"):
            domain_move_out_loc = expression.AND(
                [domain_move_out_loc, [("location_dest_id.usage", "=", "customer")]]
            )
        return domain_quant_loc, domain_move_in_loc, domain_move_out_loc


class ProductTemplate(models.Model):
    _inherit = "product.template"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog.web",
        relation="catalog_web_product_template_rel",
        column1="product_tmpl_id",
        column2="catalog_id",
        string="Catalogs",
    )
    internal_category_id = fields.Many2one(
        comodel_name="internal.product.category",
        string="Internal Category",
    )
    serie_id = fields.Many2one(
        comodel_name="product.series",
        string="Product serie",
    )
    list_price_tax = fields.Float(
        string="PVP with tax",
        compute="_compute_list_price_tax",
        store=True,
    )
    b2b_virtual_available = fields.Float(
        string="B2B Quantity",
        compute="_compute_b2b_quantities",
        digits="Product Unit of Measure",
        compute_sudo=True,
    )

    def _compute_b2b_quantities(self):
        for template in self:
            template.b2b_virtual_available = sum(
                template.product_variant_ids.mapped("b2b_virtual_available")
            )

    @api.depends("list_price", "taxes_id")
    def _compute_list_price_tax(self):
        for template in self:
            if template.taxes_id:
                tax = template.taxes_id.compute_all(
                    template.list_price,
                    currency=template.currency_id,
                    quantity=1.0,
                    product=template.product_variant_id,
                    partner=False,
                )
                template.list_price_tax = tax["total_included"]
            else:
                template.list_price_tax = template.list_price


class ProductCatalogWeb(models.Model):
    _name = "product.catalog.web"
    _description = "Product Catalog web"

    @api.model
    def _default_warehouse_id(self):
        return self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )

    active = fields.Boolean(default=True)
    commitment_date = fields.Datetime(
        help=(
            "This is the delivery date promised to the customer. If set, the "
            "delivery order will be scheduled based on this date rather than "
            "product lead times."
        ),
    )
    description = fields.Text(translate=True)
    logo = fields.Binary(string="Logo File")
    visible_slider = fields.Boolean(string="Visible in Website", default=True)
    inventory_availability = fields.Selection(
        [
            ("never", "Sell regardless of inventory"),
            (
                "always",
                "Show inventory on website and prevent sales if not enough stock",
            ),
            (
                "threshold",
                "Show inventory below a threshold and prevent sales if not "
                "enough stock",
            ),
            ("custom", "Show product-specific notifications"),
        ],
        default="never",
        help="Adds an inventory availability status on the web product page.",
    )
    name = fields.Char(required=True)
    date_start = fields.Date(string="Start Date", help="Starting date for the Catalog")
    date_end = fields.Date(string="End Date", help="Ending valid for the Catalog")
    season_ids = fields.Many2many(comodel_name="product.season", string="Seasons")
    pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        relation="catalog_web_product_pricelist_rel",
        column1="catalog_id",
        column2="pricelist_id",
        string="Pricelist applied",
    )
    product_ids = fields.Many2many(
        comodel_name="product.template",
        relation="catalog_web_product_template_rel",
        column1="catalog_id",
        column2="product_tmpl_id",
        string="Products",
    )
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        required=True,
        default=_default_warehouse_id,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog.web",
        relation="catalog_web_product_pricelist_rel",
        column1="pricelist_id",
        column2="catalog_id",
        string="Catalogs",
    )
    product_ids = fields.Many2many(
        comodel_name="product.template",
        string="Products",
        compute="_compute_catalog_products",
        compute_sudo=True,
        store=True,
    )
    inventory_availability = fields.Selection(
        [
            ("never", "Sell regardless of inventory"),
            (
                "always",
                "Show inventory on website and prevent sales if not enough stock",
            ),
            (
                "threshold",
                "Show inventory below a threshold and prevent sales if not "
                "enough stock",
            ),
            ("custom", "Show product-specific notifications"),
        ],
        help=(
            "Esto tiene mayor prioridad sobre el catalog. Dejar vacio para "
            "tomar dato del catalogo"
        ),
    )
    show_pvp = fields.Boolean(string="Show PVP and hide prices")
    block_sale = fields.Boolean(string="Bloquear ventas")

    @api.depends(
        "catalog_ids",
        "catalog_ids.product_ids",
        "item_ids",
        "item_ids.product_id",
        "item_ids.product_id.product_tmpl_id",
        "item_ids.product_tmpl_id",
    )
    def _compute_catalog_products(self):
        for pricelist in self:
            catalog_products = pricelist.catalog_ids.product_ids
            item_products = (
                pricelist.item_ids.product_id.product_tmpl_id
                | pricelist.item_ids.product_tmpl_id
            )
            pricelist.product_ids = catalog_products & item_products


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    pvp_price = fields.Float(string="Pricelist RRP")
