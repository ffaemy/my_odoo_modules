{
    "name": "Custom KPI Dashboard",
    "version": "18.0.1.0.0",
    "category": "Reporting",
    "summary": "Dynamic Sales & Inventory KPI Dashboard",
    "description": "Custom dashboard for real-time Sales and Inventory analytics in Odoo 18.",
    "author": "Your Name",
    "depends": ["sale", "stock", "web"],
    "data": [
        "views/dashboard_view.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "dashboard_kpi/static/src/css/dashboard.css",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
