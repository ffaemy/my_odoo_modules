# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    payment_count = fields.Integer(compute='compute_count_payments')
    advance_percent = fields.Integer("Paid %", compute='compute_payments')
    advance_payment = fields.Monetary("Paid Amount", compute='compute_payments')
    unpaid_amount = fields.Monetary("Unpaid Amount", compute='compute_payments')
    unpaid_percent = fields.Integer("Unpaid %", compute='compute_payments')

    @api.depends("partner_id")
    def compute_payments(self):
        for i in self:
            obj = self.env['account.payment'].search([('partner_id', '=', i.partner_id.id),('state', '=', 'posted')])
            if obj:
                print("obj", obj)
            total = 0
            for j in obj:
                if j.ref==i.name or j.origin_no==i.name:
                    total = total + j.amount
            i.advance_payment = total
            i.unpaid_amount = i.amount_total - total
            i.advance_percent = (i.advance_payment / (i.amount_total or 1) * 100)
            i.unpaid_percent = 100 - i.advance_percent

    @api.depends("partner_id")
    def compute_count_payments(self):
        for i in self:
            count = self.env['account.payment'].search_count([('origin_no', '=', i.name), ('state', '=', 'posted')])
            i.payment_count = count

    def action_show_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Advance Payments',
            'view_id': self.env.ref('account.view_account_payment_tree', False).id,
            'target': 'current',
            'domain': [('origin_no', '=', self.name)],
            'res_model': 'account.payment',
            'views': [[False, 'tree'], [False, 'form']],
            'context': {'default_partner_id': self.partner_id.id, 'default_origin_no': self.name,'create': False}
        }



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_count = fields.Integer(compute='compute_count_payments')
    advance_percent = fields.Integer("Paid %", compute='compute_payments')
    advance_payment = fields.Monetary("Paid Amount", compute='compute_payments')
    unpaid_amount = fields.Monetary("Unpaid Amount", compute='compute_payments')
    unpaid_percent = fields.Integer("Unpaid %", compute='compute_payments')

    @api.depends("partner_id")
    def compute_payments(self):
        for i in self:
            obj = self.env['account.payment'].search([('partner_id', '=', i.partner_id.id),('state', '=', 'posted')])
            if obj:
                print("purchaseorder obj", obj)
            total = 0
            for j in obj:
                if j.ref == i.name or j.origin_no == i.name:
                    total = total + j.amount
            i.advance_payment = total
            i.unpaid_amount = i.amount_total - total
            i.advance_percent = (i.advance_payment / (i.amount_total or 1) * 100)
            i.unpaid_percent = 100 - i.advance_percent



    @api.depends("partner_id")
    def compute_count_payments(self):
        for i in self:
            count = self.env['account.payment'].search_count([('origin_no', '=', i.name), ('state', '=', 'posted')])
            print(count)
            i.payment_count = count





    def action_show_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Advance Payments',
            'view_id': self.env.ref('account.view_account_payment_tree', False).id,
            'target': 'current',
            'domain': [('origin_no', '=', self.name)],
            'res_model': 'account.payment',
            'views': [[False, 'tree'], [False, 'form']],
            'context': {'default_partner_id': self.partner_id.id, 'default_origin_no': self.name,'create': False}
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    advance_percent = fields.Integer("Paid %", compute='compute_payments')
    advance_payment = fields.Monetary("Paid Amount", compute='compute_payments')
    unpaid_amount = fields.Monetary("Unpaid Amount", compute='compute_payments')
    unpaid_percent = fields.Integer("Unpaid %", compute='compute_payments')

    @api.depends("partner_id")
    def compute_payments(self):
        for i in self:
            obj = self.env['account.payment'].search([('ref', '=', i.name), ('state', '=', 'posted')])
            print("obj",obj)
            total = 0
            for j in obj:
                total = total + j.amount
            i.advance_payment = total
            i.unpaid_amount = i.amount_total-total
            i.advance_percent=(i.advance_payment/(i.amount_total or 1)*100)
            i.unpaid_percent=100-i.advance_percent


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'
    description= fields.Text(string="Description")
    origin_no = fields.Char(string="Origin")

    def action_post(self):
        res = super(AccountPaymentInh, self).action_post()
        self._onchange_payments()

        return res


    def _onchange_payments(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        obj = self.env['account.move'].search([('id', '=', rec_model.id)])
        if not self.origin_no:
            self.origin_no = obj.invoice_origin
            print(obj.invoice_origin)



