{
    'name': 'Custom Search Views',
    'version': '18.0.0.0.1',
    'category': 'Tools',
    'summary': 'Demonstration of Advanced Search Views in Odoo 18',
    'author': 'Odooistic',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',                  # second: apply access rights
        'views/custom_search_demo_views.xml',
        'views/custom_search_demo_search_view.xml',

    ],
    'installable': True,
    'application': True,
}
