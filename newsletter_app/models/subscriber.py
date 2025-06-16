from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

class Subscriber(models.Model):
    _name = 'newsletter.subscriber'
    _description = 'Newsletter Subscriber'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    email = fields.Char(required=True, tracking=True)
    category_ids = fields.Many2many('subscription.category', string='Categories', tracking=True)
    active = fields.Boolean(default=True, tracking=True)

    @api.constrains('email')
    def _check_valid_email(self):
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            if not re.match(email_regex, record.email):
                raise ValidationError('Please enter a valid email address.')
