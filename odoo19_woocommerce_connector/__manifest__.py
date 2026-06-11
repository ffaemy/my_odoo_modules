{
    "name": "Odoo 19 WooCommerce Connector",
    "version": "19.0.1.0.0",
    "category": "Sales/Integrations",
    "summary": "Connect Odoo 19 with WooCommerce: import products, customers, orders and booking appointments",
    "description": """
Odoo 19 WooCommerce Connector for tutorial/demo usage.

Features:
- WooCommerce settings section in Odoo Settings
- Store URL, Consumer Key, Consumer Secret
- Test connection button
- Import WooCommerce products into Odoo products
- Import WooCommerce customers into Odoo contacts
- Import WooCommerce orders into Odoo sales orders
- Create calendar appointments from WooCommerce booking metadata
""",
    "author": "Odooistic",
    "website": "https://odooistic.co.uk",
    "depends": ["base", "sale_management", "stock", "account", "calendar"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
