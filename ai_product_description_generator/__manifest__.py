{
    "name": "AI Product Description Generator",
    "version": "19.0.1.0.0",
    "category": "Productivity",
    "summary": "Generate product descriptions using AI in Odoo 19",
    "author": "Odooistic",
    "depends": ["product", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}