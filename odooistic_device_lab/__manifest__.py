{
    "name": "Odooistic Device Lab",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "summary": "ORM cache, prefetching, flush and raw SQL demonstration",
    "description": """
Odooistic Device Lab
====================

A practical Odoo 19 tutorial module demonstrating:

* ORM record cache
* Recordset prefetching
* flush_model()
* Raw SQL with RETURNING
* invalidate_recordset()
* modified()
* Stored computed-field dependencies
    """,
    "author": "Odooistic",
    "website": "https://www.odooistic.co.uk",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/device_asset_views.xml",
        "views/device_asset_menus.xml",
        "data/device_asset_data.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}