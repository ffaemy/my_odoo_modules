{
    'name': 'Custom Asset Management',
    'summary': 'First Odoo 18 module',
    'description': '''
        Testing Purpuses.
    ''',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'license': 'LGPL-3', 
    'author': 'Odooistic',
    'website': 'http://www.odooistic.co.uk',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        
        'security/ir.model.access.csv',
        'views/asset_asset_views.xml',
        'views/asset_category_views.xml',
        'views/menus.xml',
        
    ],
    
    'installable': True,
    'application': True,

}
