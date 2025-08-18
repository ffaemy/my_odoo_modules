{
    "name": "OWL Task Notification Widget",
    "version": "1.0",
    "depends": [
        "base", 
        "web", 
        "project"
        ],
    "author": "Odooistic",
    "category": "Tools",
    "summary": "Owl widget to display recent project tasks as notifications",
    "assets": {
    "web.assets_backend": [
        "owl_notification_widget/static/src/js/task_notification_widget.js",
        "owl_notification_widget/static/src/xml/task_notification_widget.xml",
    ],
},
    "installable": True,
    "application": False,
}
