# -*- coding: utf-8 -*-
{
    'name': "Purchase Taxes",

    'summary': """
        Purchase Taxes""",

    'description': """
        Purchase Taxes
    """,

    'author': "Hunain Ak",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/purchase_tax_wizard.xml',
        'views/views.xml',
    ],
	'images': ['static/description/icon.png'],

}
