{
    "name": "Approval System",
    "version": "18.0.1.0.0",
    "category": "Sales Management",
    "summary": "Implements a role-based approval system for sales orders.",
    "description": """
        This module customizes Odoo's user roles and permissions to create an approval system 
        for sales orders. It introduces a multi-level approval process where Salespeople can 
        create sales orders, but only Sales Managers can approve them before confirmation.

        Key Features:
        - Custom user roles: Salesperson, Sales Manager, Administrator.
        - Salesperson can create and edit orders but cannot confirm them.
        - Sales Manager can approve and confirm sales orders.
        - Record rules and access control lists (ACLs) for security.
        - Automated notifications to managers for order approvals.

        This module ensures better control over the sales process, preventing unauthorized 
        order confirmations and ensuring a proper approval workflow.
    """,
    "author": "Odooistic",
    "depends": [
        "sale_management",
        "base",
    ],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
