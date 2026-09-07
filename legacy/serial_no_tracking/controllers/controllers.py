# -*- coding: utf-8 -*-
# from odoo import http


# class SerialNoTracking(http.Controller):
#     @http.route('/serial_no_tracking/serial_no_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/serial_no_tracking/serial_no_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('serial_no_tracking.listing', {
#             'root': '/serial_no_tracking/serial_no_tracking',
#             'objects': http.request.env['serial_no_tracking.serial_no_tracking'].search([]),
#         })

#     @http.route('/serial_no_tracking/serial_no_tracking/objects/<model("serial_no_tracking.serial_no_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('serial_no_tracking.object', {
#             'object': obj
#         })
