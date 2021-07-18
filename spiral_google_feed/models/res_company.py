# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    google_age_group = fields.Many2one('product.attribute', string='Age Group')
    google_color = fields.Many2one('product.attribute', string='Colour')
    google_gender = fields.Many2one('product.attribute', string='Gender')
    google_material = fields.Many2one('product.attribute', string='Material')
    google_size = fields.Many2one('product.attribute', string='Size')