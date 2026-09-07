{
    "name": "Product eBay Fields",
    "version": "18.0.1.0.0",
    "category": "Ebay Connectivity",
    "summary": "Add eBay-related fields to Odoo products.",
    "description": """
        This module enhances the Odoo product model by adding eBay-related fields to store 
        essential eBay listing details. It allows users to manage eBay-specific attributes, 
        such as the item number, listing status, price, stock availability, and listing URL 
        directly from the Odoo product form. 

        Key Features:
        - Adds eBay Item Number field for unique identification.
        - Includes eBay Listing Status (Active, Draft, Ended, Pending).
        - Stores eBay-specific Price and Stock availability.
        - Provides a field for the eBay Listing URL for quick access.
        - Seamlessly integrates with Odoo’s existing product management system.

        This module serves as a foundation for future integration with the eBay API to 
        automate listing updates and synchronize inventory levels.
    """,
    "author": "Odooistic",
    "depends": ["product"],
    "data": [
        "views/product_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
