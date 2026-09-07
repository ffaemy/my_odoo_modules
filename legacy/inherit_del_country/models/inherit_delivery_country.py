# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class InheritDeliveryCountry(models.Model):
    _inherit = 'account.invoice'

    delivery_country = fields.Char(string="Delivery Country", compute="_get_delivery_country_name")


    def _get_delivery_country_name(self):
        for order in self:
            del_country = self.env['sale.order'].search([('name', '=', order.origin)])
            order.delivery_country = del_country.delivery_country
