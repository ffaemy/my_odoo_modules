{
    "name": "Cron Management",
    "version": "18.0.1.0.0",
    "category": "Automation",
    "summary": "Implements scheduled tasks (cron jobs) in Odoo.",
    "description": """
        This module provides functionality to create and manage scheduled actions (cron jobs) in Odoo.
        It automates tasks such as archiving old records, sending scheduled emails, and system maintenance.
    """,
    "author": "Odooistic",
    "depends": [
        "base",
    ],
    "data": [
        "data/scheduled_action.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
