{
    'name': 'Odoo 17 Custimizations',
    'version': '1.0',
    'category': 'Tools',
    'description': 'Fetch and store weather data via API',
    'depends': [
        'base',
        'website',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
    ],

    'assets': {
        
        'web.assets_backend': [
            'customization/static/src/scss/product_template.scss',
        ],
    },
    

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}