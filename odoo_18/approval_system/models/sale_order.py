from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved')
    ], string="Approval Status", default="draft", tracking=True)

    def request_approval(self):
        """ Salesperson requests approval from Sales Manager """
        if self.approval_state != 'draft':
            raise UserError("Approval can only be requested when the order is in Draft state.")
        
        self.write({'approval_state': 'waiting'})

        # Notify all sales managers
        managers = self.env.ref('approval_system.group_sales_manager').users
        for manager in managers:
            self.message_post(
                body=f"Sales Order {self.name} is awaiting approval.",
                partner_ids=[manager.partner_id.id]
            )

    def approve_order(self):
        """ Sales Manager approves the order and allows confirmation """
        if self.approval_state != 'waiting':
            raise UserError("Only orders in 'Waiting for Approval' state can be approved.")
        
        self.write({'approval_state': 'approved'})
        super(SaleOrder, self).action_confirm()  # Call Odoo’s default confirmation method
