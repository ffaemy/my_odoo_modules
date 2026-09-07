# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woudedsouls.co.uk>
# All Rights Reserved.
##########################################################################

{
    'name': "inherit_del_country",
    'summary': """
        Module to get Delivery Country Field on Tree Name: account.invoice.tree""",
    'description': """
        Module to get Delivery Country Field on Tree Name: account.invoice.tree
        where external ID is account.invoice_tree_with_onboarding""",
    'author': "Muhammad Farooq Rajput",
    'website': "http://www.woudedsouls.co.uk",
    'category': 'Spiral Module Customization',
    'version': 'Feb2021001',
    'depends':  ['base','account'],
    'data':     [
        'views/inherit_delivery_country_ontree.xml',
                ],
    "application"          :  True,
}