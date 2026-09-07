# -*- coding: utf-8 -*-
from odoo import http

# class PuroNatural1(http.Controller):
#     @http.route('/puro_natural1/puro_natural1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/puro_natural1/puro_natural1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('puro_natural1.listing', {
#             'root': '/puro_natural1/puro_natural1',
#             'objects': http.request.env['puro_natural1.puro_natural1'].search([]),
#         })

#     @http.route('/puro_natural1/puro_natural1/objects/<model("puro_natural1.puro_natural1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('puro_natural1.object', {
#             'object': obj
#         })