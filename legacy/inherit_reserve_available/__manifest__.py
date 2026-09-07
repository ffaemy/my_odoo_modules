# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woundedsouls.co.uk>
# All Rights Reserved.
##########################################################################
{
    'name': "inherit_reserve_available",
    'summary': """
        Module to inherit Reserve Quantity & Available quantity""",
    'description': """
        Module to inherit Reserve Quantity & Available quantity on Product and Product Varient""",
    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woundedsouls.co.uk",
    'category': 'Module customization',
    'version': 'Mar2021002',
    'depends': ['base','product','stock'],
    'data':     [
        'views/views.xml',
        'views/templates.xml',
                ],
    'application'          :  True,
}