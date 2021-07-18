# -*- coding: utf-8 -*-
from odoo import http

# class InheritPurchaseSale(http.Controller):
#     @http.route('/inherit_purchase_sale/inherit_purchase_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_purchase_sale/inherit_purchase_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_purchase_sale.listing', {
#             'root': '/inherit_purchase_sale/inherit_purchase_sale',
#             'objects': http.request.env['inherit_purchase_sale.inherit_purchase_sale'].search([]),
#         })

#     @http.route('/inherit_purchase_sale/inherit_purchase_sale/objects/<model("inherit_purchase_sale.inherit_purchase_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_purchase_sale.object', {
#             'object': obj
#         })