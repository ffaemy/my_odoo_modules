# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_age_group = fields.Many2one('product.attribute', string='Age Group', related='company_id.google_age_group', readonly=False)
    google_color = fields.Many2one('product.attribute', string='Colour', related='company_id.google_color', readonly=False)
    google_gender = fields.Many2one('product.attribute', string='Gender', related='company_id.google_gender', readonly=False)
    google_material = fields.Many2one('product.attribute', string='Material', related='company_id.google_material', readonly=False)
    google_size = fields.Many2one('product.attribute', string='Size', related='company_id.google_size', readonly=False)