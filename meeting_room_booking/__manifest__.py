{
    'name': 'Meeting Room Booking',
    'summary': 'App to manage and book meeting rooms.',
    'description': '''
        Manage meeting rooms, book schedules, and prevent double bookings.
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
        'views/room_views.xml',
        'views/booking_views.xml',
        'views/actions.xml',
        'views/menus.xml',
        
    ],
    
    'installable': True,
    'application': True,

}
