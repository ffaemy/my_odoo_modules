from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_order_count = fields.Integer(
        string="Sale Order Count",
        compute='_compute_sale_order_count'
    )

    def _compute_sale_order_count(self):
        for product in self:
            product.sale_order_count = self.env['sale.order.line'].search_count([
                ('product_id', '=', product.id)
            ])

    def action_view_sale_orders(self):
        self.ensure_one()
        sale_orders = self.env['sale.order.line'].search([
            ('product_id', '=', self.id)
        ]).mapped('order_id')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', sale_orders.ids)],
            'context': {'default_product_id': self.id},
            'target': 'current',
        }

