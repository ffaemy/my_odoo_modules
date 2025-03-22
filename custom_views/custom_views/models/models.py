from odoo import models, fields

class CustomRecord(models.Model):
    _name = 'custom.record'  # This defines the model name
    _description = 'Custom Record Example'

    # Fields to store data in the model
    name = fields.Char(string='Record Name', required=True)  # Name of the record
    description = fields.Text(string='Description')  # Description text
    date = fields.Datetime(string='Date')  # Date and time field
    amount = fields.Float(string='Amount')  # Numeric field to store amount
