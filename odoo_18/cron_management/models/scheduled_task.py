from odoo import models, fields, api


class ScheduledTask(models.Model):
    _name = 'custom.automation.task'
    _description = 'Automated Task Example'

    @api.model
    def auto_archive_orders(self):
        """
        This function automatically archives sales orders older than 6 months.
        """
        orders = self.env['sale.order'].search([
            ('date_order', '<', fields.Datetime.subtract(fields.Datetime.now(), months=6)),
            ('state', 'in', ['draft', 'sale'])
        ])
        
        for order in orders:
            order.write({'active': False})  # Archiving the record
        
