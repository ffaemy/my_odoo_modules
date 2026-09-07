from odoo import models, fields

class SubscriptionCategory(models.Model):
    _name = 'subscription.category'
    _description = 'Newsletter Subscription Category'

    name = fields.Char(required=True)
    description = fields.Text()


    def action_view_subscribers(self):
        return {
            'name': 'Subscribers',
            'type': 'ir.actions.act_window',
            'res_model': 'newsletter.subscriber',
            'view_mode': 'list,form',
            'domain': [('category_ids', 'in', self.ids)],
            'target': 'current',
        }