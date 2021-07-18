# -*- coding: utf-8 -*-
from odoo import http

# class InheritReserveAvailable(http.Controller):
#     @http.route('/inherit_reserve_available/inherit_reserve_available/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_reserve_available/inherit_reserve_available/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_reserve_available.listing', {
#             'root': '/inherit_reserve_available/inherit_reserve_available',
#             'objects': http.request.env['inherit_reserve_available.inherit_reserve_available'].search([]),
#         })

#     @http.route('/inherit_reserve_available/inherit_reserve_available/objects/<model("inherit_reserve_available.inherit_reserve_available"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_reserve_available.object', {
#             'object': obj
#         })