# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class inherit_reserve_available(models.Model):
    _inherit = 'product.template'

    product_line = fields.One2many("product.line","line_id", string="Product")
    product_bundle = fields.Boolean(string="Add Product Bundle")
    bundle_name = fields.Char(string="Bundle Name")
    net_total = fields.Float(string="Net Total" ,compute="compute_total")
    net_total_val = fields.Text(string="Bundle Total")

    @api.depends("product_line.total")
    def compute_total(self):
        total = 0
        for i in self.product_line:
            total = total + i.total
        self.update({
            'net_total': total})

    def action_compute_bundle(self):
        self.net_total_val = self.net_total


class inherit_line(models.Model):
    _name = 'product.line'

    line_id = fields.Many2one('product.template')
    product_desc = fields.Many2one("product.product", string="Product Description")
    quantity = fields.Integer("Quantity")
    unit_price = fields.Float("Unit Price")
    total = fields.Float("Total")
    discount = fields.Float("Discount")

    @api.onchange("product_desc")
    def onchange_product(self):
        self.unit_price = self.product_desc.list_price

    @api.onchange("quantity")
    def onchange_quantity(self):
        for i in self:
            self.total = i.unit_price * i.quantity

    def action_compute_bundle(self):
        self.net_total_val = self.product_line.net_total





