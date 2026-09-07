from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    woo_id = fields.Char(string="WooCommerce ID", copy=False, index=True)
    woo_sku = fields.Char(string="WooCommerce SKU", copy=False)
    woo_sync_date = fields.Datetime(string="WooCommerce Last Sync", copy=False)
