# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class inherit_reserve_available(models.Model):
    _inherit = 'product.template'

    reserved_quantity = fields.Float("Reserved Quantity", compute="onchange_reserve")
    available_quantity = fields.Float("Available Quantity", related= "qty_available")
    cash_price = fields.Float(string="Cash Price" ,compute="cash_price_func")
    walk_in = fields.Float(string="Walk In Price", compute="walk_in_func")

    def walk_in_func(self):
        for rec in self:
            rec.walk_in = 0
            walk_price = self.env['product.pricelist'].search([])
            for obj in walk_price:
                if obj.name == 'Walk In':
                    for loop in obj.item_ids:
                        if rec.name == loop.name:
                            rec.walk_in = float(loop.fixed_price)

    def cash_price_func(self):
        for res in self:
            res.cash_price = 0
            cash_p = self.env['product.pricelist'].search([])
            for obj in cash_p:
                if obj.name == 'Cash':
                    for loop in obj.item_ids:
                        if res.name == loop.name:
                            res.cash_price = float(loop.fixed_price)






        #self.cash_price = cash_p.price

    def onchange_reserve(self):
        for res in self:
            reserve_qty = self.env['stock.quant'].search([('product_id', '=', self.id)])
            for obj in reserve_qty:
                res.reserved_quantity += obj.reserved_quantity





# class inherit_whout_reserved(models.Model):
#     _inherit = 'stock.move'
#
#     res_qty = fields.Float("Reserved Quantity", related = "product_id.reserved_quantity")







