# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woudedsouls.co.uk>
# All Rights Reserved.
##########################################################################
{
    'name': "Inovice/Bill Origin",

    'summary': """THis module is developed for Showing Origin number at payments""",

    'description': """THis module is developed for Showing Origin number at payments""",

    'author': "Wounded Souls",
    'website': "http://www.woundedsouls.co.uk",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
