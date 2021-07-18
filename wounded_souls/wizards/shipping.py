# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class WoundedOrderLineShipping(models.TransientModel):
    _name = "wounded_shipping_wizard"

    shipping_name = fields.Char(string="Shipping Name")
    shipping_value = fields.Float(string="Shipping Cost")

    def update_shipping(self):
        # print('Context:', self.env.context)
        # print('Active ID:', self.env.context.get('active_id'))
        # print('Shipping Name:', self.shipping_name)
        # print('Shipping Value:', self.shipping_value)
        #
        active_id = self.env.context.get('active_id')
        object = self.env['product.product'].search([('name' ,'=', self.shipping_name)], limit=1)
        if not object:
                object1 = self.env['product.template'].create({
                'name': self.shipping_name
            })

        obj = self.env['wounded.souls.orderline'].create({

            'order_id': active_id,
            'name': object.id,
            'sell_price': self.shipping_value
        })

