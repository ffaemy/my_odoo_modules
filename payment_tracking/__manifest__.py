# -*- coding: utf-8 -*-
##########################################################################
# Author      : Muhammad Farooq Rajput
# Copyright 2021 @Wounded Souls <http://www.woudedsouls.co.uk>
# All Rights Reserved.
##########################################################################

{
    'name': "Payment Tracking in PO,SO,Invoices",

    'summary': """
       Track payments in increments for purchases
       Track payments in increments for sales
        Track payments in increments for invoices
""",

    'description': """
        We added 3 states to calculate paid amount,paid %, unpaid Amount and unpaid %. 
    """,

    'author': "info@woundedsouls.co.uk",
    'website': "www.woundedsouls.co.uk",
    'license': 'WS234-1',
    'images': ['static/description/sukkela_200_high_rounded.png'],

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account','purchase'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
