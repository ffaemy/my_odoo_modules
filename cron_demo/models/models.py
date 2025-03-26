from odoo import models, fields

class CustomRecord(models.Model):
    _name = 'custom.record'
    _description = 'Custom Record'

    name = fields.Char(string='Record Name', required=True)
    status = fields.Selection([('draft', 'Draft'), ('completed', 'Completed')], default='draft')

    def update_status(self):
        records = self.search([('status', '=', 'draft')])  # Find all draft records
        for record in records:
            record.status = 'completed'  # Change status to completed
