# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OrderLineShipping(models.TransientModel):
    _name = "shipping_wizard"

    shipping_name = fields.Char(string="Shipping Name")
    shipping_value = fields.Float(string="Shipping Cost")


    # @api.model
    # def default_get(self, fields):
    #     res = super(OrderLineShipping, self).default_get(fields)
    #
    #     active_id = self.env.context.get('active_id')
    #     order_id = self.env['sale.order'].search([('id', '=', active_id)], limit=1)
    #     if order_id:
    #         res.update({
    #         'order_id': order_id and order_id.id or False,
    #     })
    #     return res

    def update_shipping(self):
        print('context', self.env.context)
        print('active_id', self.env.context.get('active_id'))
        print('shipping name',self.shipping_name)
        print('shipping value', self.shipping_value)

        active_id = self.env.context.get('active_id')
        query_id = self.env['sale.order'].search([('id', '=', self.env.context.get('active_id'))],limit=1)

        print(query_id)

        object = self.env['product.product'].search([('name' ,'=', self.shipping_name)], limit=1)
        print(object.name)
        if not object:


                onject1 = self.env['product.template'].create({
                'name' : self.shipping_name
            })

        obj=self.env['sale.order.line'].create({

            'order_id': active_id,
            'product_id': object.id ,
            'price_unit': self.shipping_value
        })
        print(object.id)





