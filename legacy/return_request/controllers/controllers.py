# -*- coding: utf-8 -*-
# from odoo import http


# class Bash(http.Controller):
#     @http.route('/bash/bash/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bash/bash/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bash.listing', {
#             'root': '/bash/bash',
#             'objects': http.request.env['bash.bash'].search([]),
#         })

#     @http.route('/bash/bash/objects/<model("bash.bash"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bash.object', {
#             'object': obj
#         })
