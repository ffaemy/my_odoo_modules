{
    'name': 'Interactive Newsletter Subscription',
    'version': '18.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Manage newsletter subscriptions with email validation and chatter integration.',
    'description': """
        This module allows users to subscribe to newsletters categorized by topics. 
        Features include email validation, subscription toggles, security rules, and chatter notifications.
    """,
    'depends': ['base', 'mail', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/subscriber_views.xml',
        'views/subscriber_mail_wizard_view.xml',
        'views/subscription_category_views.xml',
        'views/newsletter_menu.xml',
        'views/subscription_category_views.xml',
        'data/subscription_category_data.xml',
    ],
    
    'author': 'Odooistic',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
