{
    "name": "Odoo 19 REST API Demo",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "summary": "Demo REST API endpoints for Odoo 19 integrations",
    "description": """
Odoo 19 REST API Demo module for YouTube/tutorial usage.

Features:
- API key stored in Settings
- GET products endpoint
- POST customer creation endpoint
- POST sale order creation endpoint
- Clean JSON responses
""",
    "author": "Odooistic",
    "website": "https://odooistic.co.uk",
    "depends": ["base", "sale", "product"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
