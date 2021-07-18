# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woudedsouls.co.uk>
# All Rights Reserved.
##########################################################################

{
    'name': "effective_date",
    'summary': """
        Module to get Effective Date Field on Sales Orders Tree and add some fields 
	in Trade Export File""",
    'description': """
        Module to get Effective Date Field on Sales Orders Tree and add some fields 
	in Trade Export File""",
    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woudedsouls.co.uk",
    'category': 'Spiral Module Customization',
    'version': 'WS65777',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
