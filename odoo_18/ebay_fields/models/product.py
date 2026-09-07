from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ebay_item_number = fields.Char(string="eBay Item Number", help="Unique eBay Item ID")
    ebay_listing_status = fields.Selection([
        ('active', 'Active'),
        ('ended', 'Ended'),
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ], string="eBay Listing Status", default='draft')
    ebay_price = fields.Float(string="eBay Price", help="Price of the product on eBay")
    ebay_stock = fields.Integer(string="eBay Stock", help="Stock available on eBay")
    ebay_listing_url = fields.Char(string="eBay Listing URL", help="Direct link to eBay listing")

