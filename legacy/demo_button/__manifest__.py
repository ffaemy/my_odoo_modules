{
    "name": "Demo Button",
    "version": "1.0",
    "author": "Odooistic",
    "website": "https://www.odooistic.com",
    "category": "Tools",
    "summary": "A simple module showing how to add a button",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/demo_model_views.xml",
    ],
    "images": ["static/description/icon.png"],  # 👈 ADD THIS
    "installable": True,
    "application": True,   # 👈 REQUIRED TO SHOW APP ON DASHBOARD
}
