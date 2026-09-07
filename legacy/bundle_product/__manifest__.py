# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woundedsouls.co.uk>
# All Rights Reserved.
##########################################################################
{
    'name': "bundle_product",
    'summary': """
        Module to have bundle products""",
    'description': """
        Module to have bundle products""",
    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woundedsouls.co.uk",
    'category': 'Module customization',
    'version': 'Mar2021004',
    'depends': ['base','purchase','stock','sale'],
    'data':     [
        'security/ir.model.access.csv',
        'views/views.xml',
                ],
    'application'          :  True,
}