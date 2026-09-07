{
    'name': 'Project / FSM Calendar Assignee Filter',
    'version': '18.0.0.1',
    'category': 'Extra Tools',
    "author": 'M Farooq Rajput (farooq.rajput@gravitai.com)',   
    "summary": "Add Assignees (user_ids) as a sidebar filter in the Field Service calendar",
    "description": """
    This module extends the Field Service Management (FSM) calendar view
    so that tasks can be filtered by Assignees (user_ids) in the right-hand filter panel.

    Features:
    - Adds an "Assignees" filter to the FSM calendar.
    - Persists filter selections per user using a helper model.
    - Shows user avatars in the filter list.
        """,
    'depends': ['web', 'project'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/inherit_task_calendar.xml',
    ],
}
