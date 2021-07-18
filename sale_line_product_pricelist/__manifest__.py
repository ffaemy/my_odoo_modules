# -*- coding: utf-8 -*-

{
    'name': 'Product Prices On Sale Line',
    'version': '1.0',
    'summary': "Product Price On Sale Line",
    'description': """
Product Prices from Pricelists On Sale Line
============================================
Avail Popup to display prices of product for each line.""",
    'category': 'Sale',
    'author': 'Hunain AK',
    'depends': ['sale','stock','sale_management','product'],
    'data': [
        'views/assets_view.xml',
        'views/sale_order.xml',
        'views/product.xml',
    ],
    'qweb': ['static/src/xml/price_on_line.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,


'images': ['static/description/icon.png'],

}
