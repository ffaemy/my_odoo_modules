# -*- coding: utf-8 -*-
from odoo import http

# class EffectiveDate(http.Controller):
#     @http.route('/effective_date/effective_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/effective_date/effective_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('effective_date.listing', {
#             'root': '/effective_date/effective_date',
#             'objects': http.request.env['effective_date.effective_date'].search([]),
#         })

#     @http.route('/effective_date/effective_date/objects/<model("effective_date.effective_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('effective_date.object', {
#             'object': obj
#         })