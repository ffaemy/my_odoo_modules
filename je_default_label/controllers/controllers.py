# -*- coding: utf-8 -*-
# from odoo import http


# class JeDefaultLabel(http.Controller):
#     @http.route('/je_default_label/je_default_label/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/je_default_label/je_default_label/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('je_default_label.listing', {
#             'root': '/je_default_label/je_default_label',
#             'objects': http.request.env['je_default_label.je_default_label'].search([]),
#         })

#     @http.route('/je_default_label/je_default_label/objects/<model("je_default_label.je_default_label"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('je_default_label.object', {
#             'object': obj
#         })
