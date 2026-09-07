# -*- coding: utf-8 -*-
# from odoo import http


# class BomRevised(http.Controller):
#     @http.route('/bom_revised/bom_revised/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bom_revised/bom_revised/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bom_revised.listing', {
#             'root': '/bom_revised/bom_revised',
#             'objects': http.request.env['bom_revised.bom_revised'].search([]),
#         })

#     @http.route('/bom_revised/bom_revised/objects/<model("bom_revised.bom_revised"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bom_revised.object', {
#             'object': obj
#         })
