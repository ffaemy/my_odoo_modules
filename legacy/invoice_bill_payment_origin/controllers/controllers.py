# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceBillPaymentOrigin(http.Controller):
#     @http.route('/invoice_bill_payment_origin/invoice_bill_payment_origin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_bill_payment_origin/invoice_bill_payment_origin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_bill_payment_origin.listing', {
#             'root': '/invoice_bill_payment_origin/invoice_bill_payment_origin',
#             'objects': http.request.env['invoice_bill_payment_origin.invoice_bill_payment_origin'].search([]),
#         })

#     @http.route('/invoice_bill_payment_origin/invoice_bill_payment_origin/objects/<model("invoice_bill_payment_origin.invoice_bill_payment_origin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_bill_payment_origin.object', {
#             'object': obj
#         })
