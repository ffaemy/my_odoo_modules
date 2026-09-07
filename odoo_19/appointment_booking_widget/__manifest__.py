{
    "name": "Appointment Booking Widget",
    "summary": "Public appointment form with backend confirmation/decline workflow.",
    "version": "1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "author": "Odooistic Demo",
    "depends": ["base", "website", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "data/mail_template.xml",
        "views/appointment_views.xml",
        "views/website_templates.xml",
    ],
    "application": False,
}
