{
    'name': 'Discounted Products',
    'summary': 'Add discounts to products and filter discounted products on the shop page.',
    'description': """
        This module allows users to set discounts on products and provides a custom route to display only discounted products on the shop page.
        Features:
        - Add a discount field to products
        - Filter products with discounts on the shop page
    """,
    'version': '18.0.0.0.1',
    'category': 'Website',
    'author': 'Odooistic',
    'website': 'https://yourwebsite.com',
    'depends': ['website_sale'],
    'data': [
        'views/product_views.xml',
        'views/website_menu_views.xml',
        'views/website_sale_inherit_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}