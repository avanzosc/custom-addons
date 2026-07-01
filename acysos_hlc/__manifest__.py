{
    "name": "HLC custom",
    "version": "18.0.5.0.0",
    "summary": "Minimal HLC catalog and B2B stock support",
    "author": "Acysos S.L, AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/custom-addons",
    "depends": [
        "product",
        "product_brand",
        "sale",
        "stock",
        "website_sale_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_catalog_web_views.xml",
        "views/stock_location_views.xml",
    ],
    "installable": True,
}
