{
    "name": "OWL Kanban Color & Counters",
    "version": "18.0.1.0.0",
    "summary": "Dynamic Kanban color-coding and live counters (OWL 2)",
    "category": "Web",
    "author": "Odooistic",
    "depends": ["web", "mail", "crm", "project"],
    "assets": {
        "web.assets_backend": [
            "owl_kanban_color_counters/static/src/js/okc_boot.js",
            "owl_kanban_color_counters/static/src/js/kanban_color_counters.js",
            "owl_kanban_color_counters/static/src/scss/kanban_color_counters.scss",
        ],
    },
    "license": "LGPL-3",
    "installable": True,
}
