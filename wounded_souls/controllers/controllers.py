# -*- coding: utf-8 -*-
from odoo import http

# class WoundedSouls(http.Controller):
#     @http.route('/wounded_souls/wounded_souls/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wounded_souls/wounded_souls/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wounded_souls.listing', {
#             'root': '/wounded_souls/wounded_souls',
#             'objects': http.request.env['wounded_souls.wounded_souls'].search([]),
#         })

#     @http.route('/wounded_souls/wounded_souls/objects/<model("wounded_souls.wounded_souls"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wounded_souls.object', {
#             'object': obj
#         })