{
    'name': 'Product Smart Button: Sale Order Count',
    'version': '1.0',
    'summary': 'Add a smart button to Products showing the number of related Sale Orders.',
    'description': """
        This module adds a custom smart button to the product form view that displays the count 
        of sale orders where the product is used. Clicking the button opens a filtered list of 
        related Sale Orders. Great for sales tracking and product insights!

        Features:
        - Smart button with real-time count of related Sale Orders.
        - Opens filtered list of Sale Orders on click.
        - Cleanly integrated into the product form view.
        - Developer-friendly and easily extendable.

        Perfect for developers and Odoo users who want to enhance product visibility in Sales.
    """,
    'author': 'Odooistic',
    'website': 'https://www.youtube.com/@odooistic',
    'category': 'Sales',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_form_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
