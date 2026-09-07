# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'


    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Location Type'
      ,related="location_id.usage")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_pricelist_items = fields.Text(string="Priceslists",compute='_compute_pricelist_items')

    @api.depends('product_id')
    def _compute_pricelist_items(self):
        for line in self:
            priceslist_items_str = ''
            if line.product_id:
                priceslist_items = self.env['stock.quant'].search([('product_id', '=', line.product_id.id),('usage', '=', 'internal')])
                # priceslist_items_str = '|'.join([(item.location_id.name +" : " + str(item.quantity-item.reserved_quantity)+ " "+ str(item.product_uom_id.name)) for item in priceslist_items])
                priceslist_items_str = '|'.join([(str(item .location_id.location_id.name+"/"+item.location_id.name) +" : " + str(item.quantity-item.reserved_quantity)+ " "+ str(item.product_uom_id.name)) for item in priceslist_items])
            line.product_pricelist_items = priceslist_items_str