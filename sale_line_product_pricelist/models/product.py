# -*- coding: utf-8 -*-

import json
from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    json_popover = fields.Char('JSON data for the popover widget', compute='_compute_json_popover')
    
    def _compute_json_popover(self):
        for product in self:
            priceslist_items = self.env['stock.quant'].search([('product_id', '=', product.id),('usage', '=', 'internal')])
            priceslist_items_str = '|'.join([(str(item .location_id.location_id.name+"/"+item.location_id.name) +" : " + str(item.quantity-item.reserved_quantity)+ " "+ str(item.product_uom_id.name)) for item in priceslist_items])
            product.json_popover = json.dumps({
                'popoverTemplate': 'sale_line_product_pricelist.PopoverStockProduct',
                'product_pricelist_items': priceslist_items_str,
            })
            
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    json_popover = fields.Char('JSON data for the popover widget', compute='_compute_json_popover')
    
    def _compute_json_popover(self):
        for product in self:
            priceslist_items = self.env['stock.quant'].search([('product_id', 'in', product.product_variant_ids.ids),('usage', '=', 'internal')])
            priceslist_items_str = '|'.join([(str(item .location_id.location_id.name+"/"+item.location_id.name) +" : " + str(item.quantity-item.reserved_quantity)+ " "+ str(item.product_uom_id.name)) for item in priceslist_items])
            product.json_popover = json.dumps({
                'popoverTemplate': 'sale_line_product_pricelist.PopoverStockProduct',
                'product_pricelist_items': priceslist_items_str,
            })
                

