from odoo import models, fields, api, _

class CustomSearchDemo(models.Model):
    _name = 'custom.search.demo'
    _description = 'Custom Search Demo'
    _order = 'priority desc, date desc'
    _rec_name = 'name'

    name = fields.Char(
        string="Record Name",
        required=True,
        help="Enter the name or title for this record."
    )

    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        default='new',
        required=True,
        help="Current status of the record."
    )

    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High')
        ],
        string="Priority",
        default='1',
        help="Priority level of the record."
    )

    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        help="Relevant date for this record."
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, the record will be hidden from view."
    )
