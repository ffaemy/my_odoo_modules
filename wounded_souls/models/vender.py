# -*- coding: utf-8 -*-

from odoo import models, fields, api

class wounded_souls1(models.Model):
    _name = 'wounded.souls1'

    name = fields.Many2one("res.partner", string='Vender Name')
    address = fields.Char("Address")
    contact = fields.Integer("Contact No")
    mobile = fields.Integer("Mobile No")

    email = fields.Char("Email", compute='onchange_email_no')

    def onchange_email_no(self):
        email_obj = self.env['res.partner'].search([('id', '=', self.name.id)])
        self.email = email_obj.email

    title = fields.Char("Title")
    website = fields.Char("Website")

    origin = fields.Char("Origin")

    seller_ref = fields.Char("Seller Reference",compute='onchange_vendor_id')

    @api.onchange("name")
    def onchange_vendor_id(self):
        self.seller_ref = self.name.phone










