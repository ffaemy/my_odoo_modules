# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woundedsouls.co.uk>
# All Rights Reserved.
##########################################################################
{
    'name': "inherit_shipping_wizard",
    'summary': """
        Module to inherit sale order and line id""",
    'description': """
        Module to inherit sale order on purchase order and line id on WH Out and on purchase order line""",
    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woundedsouls.co.uk",
    'category': 'Module customization',
    'version': 'Mar20210891',
    'depends': ['base','purchase','sale'],
    'data':     [
        'wizards/shipping_wizard.xml',
        'views/views.xml',
                ],
    'application'          :  True,
}