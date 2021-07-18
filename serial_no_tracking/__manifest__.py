# -*- coding: utf-8 -*-
{
    'name': "serial_no_tracking",

    'summary': """
        Global Serial Number Tracking""",

    'description': """
        Global Serial/Lot Number Tracking
    """,

    'author': "Erum Asghar",
    'website': "http://www.yourcompany.com",

   
    'category': 'Uncategorized',
    'version': '0.1',

   
    'depends': ['base','stock','purchase','sale_management'],

   
    'data': [
        'security/ir.model.access.csv',
        'views/serial_no_tracking.xml',
        'views/wizard_assign_tracking.xml',
    ],
   
    'demo': [
        'demo/demo.xml',
    ],
}
