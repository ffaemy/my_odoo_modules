# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InovicePayment(models.Model):
    _inherit = 'account.payment'

    origin_id = fields.Char(string="Origin", required=False, )
    
    def create(self, vals):
      res = super(InovicePayment, self).create(vals)
      ref = res.ref
      d = self.env['account.move'].search([('payment_reference', '=', ref)])
      invoice_origin = d.invoice_origin
      payment_reference = d.payment_reference
      origin = self.env['account.payment'].search([('ref', '=', payment_reference)])
      origin.origin_id = invoice_origin
      return res
