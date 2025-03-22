{
    "name": "Graph Demo",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Generate graphs using custom Python code in Odoo 18",
    "description": """
        This Odoo 18 module allows users to dynamically generate and visualize graphs using custom Python code.
        Users can create and manage data via backend forms, and the module renders interactive graphs on the website based on this data.
        Ideal for reporting, analytics, and visualizing trends directly within Odoo.
    """,
    "author": "Odooistic",
    "depends": [
        "web",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/graph_demo_views.xml',
        'views/backend_views.xml',
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
