# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woudedsouls.co.uk>
# All Rights Reserved.
##########################################################################

{
    'name': "inherit_del_country",
    'summary': """
        A few components are changed on a BOM for a high-volume product. 
        How to track when BOM was changed/best practices?
        Create new product version instead? How to include sales for previous prod version on reports?""",
    'description': """
        We create a new menu to view the revised BOM of products in manufacturing under products Menu "Revised BOM"
    """,

    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woudedsouls.co.uk",
    'category': 'Spiral Module Customization',
    'version': 'WS564',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/bom.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
