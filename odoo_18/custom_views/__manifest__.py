{
    'name': 'Custom Views Example',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'views/custom_views.xml',
        'security/ir.model.access.csv',
        ],  
    'description': """
        This module demonstrates how to create and customize four essential views in Odoo 18:
        - Form View: Display detailed information for individual records.
        - Tree View: Present records in a table-like structure for easy browsing.
        - Kanban View: Use cards to visualize workflows and processes.
        - Calendar View: View records based on date fields in a calendar layout.
        
        The module provides a complete example of creating custom views and integrating them
        with your model for enhanced user experience and interaction with data in Odoo.
    """,
    'summary': 'Custom Views in Odoo 18 for Form, Kanban, Tree, and Calendar views',
    'website': 'http://yourwebsite.com',  # Replace with your own website or leave blank
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,  # Define the order of installation in case of dependencies
    'images': ['static/description/banner.png'],  # Optional: Add a module banner image
    'support': 'support@yourwebsite.com',  # Optional: Add your support email
}
