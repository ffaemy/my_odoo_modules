# -*- coding: utf-8 -*-
{
    "name": "Odooistic Price Override Wizard (OWL)",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Apply bulk discount with live totals preview on Sale Orders.",
    "author": "Odooistic",
    "license": "LGPL-3",
    "depends": ["sale", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/price_override_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "odooistic_price_override_wizard/static/src/js/price_override_action.js",
            "odooistic_price_override_wizard/static/src/js/price_override_dialog.js",
            "odooistic_price_override_wizard/static/src/xml/price_override_dialog.xml",
        ],
    },
    "installable": True,
    "application": False,
}
