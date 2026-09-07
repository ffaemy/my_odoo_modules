# -*- coding: utf-8 -*-
{
    "name": "Odooistic - Advanced PDF Branding (Odoo 19)",
    "version": "19.0.1.0.0",
    "category": "Sales/Reporting",
    "summary": "Advanced PDF report branding with custom external layout, headers/footers, dynamic titles",
    "web_icon": "odooistic_report_branding,static/description/icon.png",
    "images": ["static/description/app_icon.png"],
    "author": "Odooistic",
    "license": "LGPL-3",
    "depends": ["web", "sale", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/brand_views.xml",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "report/external_layout.xml",
        "report/sale_order_report_inherit.xml",
        "report/account_invoice_report_inherit.xml",
        "data/demo_brand.xml",
    ],
    "application": False,
    "installable": True,
}
