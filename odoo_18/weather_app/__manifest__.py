{
    'name': 'Weather Integration',
    'version': '1.0',
    'category': 'Tools',
    'description': 'Fetch and store weather data via API',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/weather.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}