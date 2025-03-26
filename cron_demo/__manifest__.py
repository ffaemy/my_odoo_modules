{
    'name': 'Cron Demo',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Your Name',
    'website': 'http://yourwebsite.com',  # Optional
    'depends': ['base'],
    'data': [
        'views/cron_demo_views.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',  # Reference to ACL file
    ],
    'installable': True,
    'application': True,
}
