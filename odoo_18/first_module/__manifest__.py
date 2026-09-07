{
    'name': 'first module', 
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
    ],
    'data': [
        
        'security/ir.model.access.csv',
        'views/first_module_views.xml',
        
    ],
    
    'installable': True,
    'application': True,

}
