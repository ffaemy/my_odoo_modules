{
    'name': 'Employee Recognition and Rewards',
    'summary': 'Track and reward employee achievements.',
    'description': """
        A custom module to manage employee recognition and rewards:
        - Track achievements
        - Assign points
        - Redeem rewards
        - Generate reports
    """,
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'license': 'LGPL-3', 
    'author': 'Odooistic',
    'website': 'http://www.odooistic.co.uk',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/achievement_views.xml',
        'views/achievement_type.xml',
        'views/reward_views.xml',
        'views/menus.xml',
        
    ],
    
    
    'installable': True,
    'application': True,

}
