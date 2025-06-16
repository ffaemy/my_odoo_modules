from odoo import models, fields, api
from odoo.exceptions import UserError

class SubscriberMailWizard(models.TransientModel):
    _name = 'subscriber.mail.wizard'
    _description = 'Send Email to Newsletter Subscribers'

    category_id = fields.Many2one('subscription.category', string="Category", required=True)
    subject = fields.Char(string="Subject", required=True)
    message = fields.Html(string="Message", required=True)

    def send_email(self):
        subscribers = self.env['newsletter.subscriber'].search([
            ('category_ids', 'in', self.category_id.id),
            ('active', '=', True),
        ])
        if not subscribers:
            raise UserError("No active subscribers found for this category.")

        for subscriber in subscribers:
            self.env['mail.mail'].create({
                'subject': self.subject,
                'body_html': self.message,
                'email_to': subscriber.email,
            }).send()
