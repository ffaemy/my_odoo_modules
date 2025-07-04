from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_count = fields.Integer(string="Sale Order Count", compute='_compute_sale_order_count')

    def _compute_sale_order_count(self):
        for partner in self:
            partner.sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', partner.id)])
