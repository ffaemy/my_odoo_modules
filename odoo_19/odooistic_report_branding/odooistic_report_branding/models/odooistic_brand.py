# -*- coding: utf-8 -*-
from odoo import api, fields, models

class OdooisticBrand(models.Model):
    _name = "odooistic.brand"
    _description = "Odooistic Brand (PDF Report Branding)"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)

    logo_large = fields.Binary(string="Large Logo")
    logo_small = fields.Binary(string="Small Logo")
    footer_logo = fields.Binary(string="Footer Logo")

    tagline = fields.Char(string="Tagline", translate=True)
    header_html = fields.Html(string="Header Details", translate=True, sanitize=True)
    footer_html = fields.Html(string="Footer Details", translate=True, sanitize=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("name_company_uniq", "unique(name, company_id)", "Brand name must be unique per company."),
    ]
