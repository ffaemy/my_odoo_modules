# -*- coding: utf-8 -*-
{
    "name": "Odooistic - Sale Order Approval Workflow (Odoo 19)",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Multi-level approval workflow for Sale Orders with rules, buttons, and security groups",
    "author": "Odooistic",
    "license": "LGPL-3",
    "depends": ["sale", "mail"],
    "data": [
        "security/approval_groups.xml",
        "security/ir.model.access.csv",
        "views/approval_rule_views.xml",
        "views/sale_order_views.xml",
    ],
    "application": False,
    "installable": True,
}
