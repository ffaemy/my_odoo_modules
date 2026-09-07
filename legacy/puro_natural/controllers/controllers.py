# -*- coding: utf-8 -*-
from odoo import http

# class PuroNatural(http.Controller):
#     @http.route('/puro_natural/puro_natural/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/puro_natural/puro_natural/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('puro_natural.listing', {
#             'root': '/puro_natural/puro_natural',
#             'objects': http.request.env['puro_natural.puro_natural'].search([]),
#         })

#     @http.route('/puro_natural/puro_natural/objects/<model("puro_natural.puro_natural"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('puro_natural.object', {
#             'object': obj
#         })