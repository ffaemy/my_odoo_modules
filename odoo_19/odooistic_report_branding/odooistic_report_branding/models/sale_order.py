# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _default_brand_id(self):
        company = self.env.company
        return self.env["odooistic.brand"].search([("company_id", "=", company.id)], limit=1)

    brand_id = fields.Many2one(
        "odooistic.brand",
        string="Brand",
        domain="[('company_id', '=', company_id)]",
        default=_default_brand_id,
        help="Brand to use for PDF layout (header/footer).",
    )
