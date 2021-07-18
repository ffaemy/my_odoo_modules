# -*- coding: utf-8 -*-
{
    'name': "wounded_souls",

    'summary': """
        Details about products available""",

    'description': """
        Stock control Module, details about products details.
    """,

    'author': "Muhammad Farooq Rajput",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'wizards/shipping.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}