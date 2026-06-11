from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    woo_id = fields.Char(string="WooCommerce ID", copy=False, index=True)
    woo_sync_date = fields.Datetime(string="WooCommerce Last Sync", copy=False)
