{
    "name": "Odoo 19 Global Smart Search",
    "summary": "Google-style global search across multiple models from one search box.",
    "version": "1.0.0",
    "author": "Odooistic",
    "website": "https://www.odooistic.co.uk",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "odoo19_global_search/static/src/js/global_search.js",
            "odoo19_global_search/static/src/css/global_search.css",
            "odoo19_global_search/static/src/xml/global_search.xml",
        ],
    },
    "installable": True,
    "application": False,
}
