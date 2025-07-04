{
    'name': 'Partner Sale Order Counter Widget',
    'version': '1.0',
    'summary': 'Shows total Sale Orders for a customer using an OWL field widget',
    'description': 'Adds a custom OWL 2 widget on res.partner form view to display number of related Sale Orders.',
    'category': 'Sales',
    'author': 'Odooistic',
    'depends': ['base', 'sale', 'web'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_partner_widget/static/src/js/widgets/sale_order_counter_widget.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
