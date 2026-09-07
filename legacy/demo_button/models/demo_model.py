from odoo import models, fields

class DemoButton(models.Model):
    _name = "demo.button"
    _description = "Demo Button Model"

    name = fields.Char(string="Name")

    def action_show_message(self):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Odooistic!",
                "message": "Button Clicked Successfully 🎉",
                "sticky": False,
            },
        }
