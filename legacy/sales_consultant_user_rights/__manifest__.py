# -*- coding: utf-8 -*-
{
    'name': "Sales User Rights",

    'summary': """
        Sales User Rights""",

    'description': """
       Showing Sale User's own customers, Removing Invoice Button for Sale User, Making Sale lines Readonly when sale order
       is confirmed.
    """,

    'author': "Viltco Technologies",
    'website': "http://www.abc.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'account', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        # 'views/stock_picking_views.xml',
        # 'data/sequence.xml',
        'data/data.xml',
    ],

}
