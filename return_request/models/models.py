# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError, ValidationError


class ReturnRequest(models.Model):
    _name = 'returns.bash'
    _description='Return Request'

    name = fields.Many2one("res.partner",string="Customer Name")
    contact_person = fields.Many2one("res.partner",string="Contact Person",domain="[('id', 'child_of',name)]")
    address = fields.Char(string="Address")
    date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())
    net_total = fields.Float("Net Total",compute="compute_total_invoice")
    request_line = fields.One2many("request.line", "request_order_line")
    state = fields.Selection([('user', 'User'), ('manager', 'Manager'),('director', 'Director'),('done', 'Validate')], string="State", readonly=True, default="user")
    user_id = fields.Many2one("res.users", string="User")

    # Onchange Function for user id
    @api.onchange("user_id")
    def onchange_discount(self):
        users = ['Marc Demo', 'Mitchell Admin', 'Joel Willis', 'Muhammad Rajput']
        for i in self.request_line:
            if self.user_id.name == users[0]:
                i.discount_qty = 10
            if self.user_id.name == users[1]:
                i.discount_qty = 12
            if self.user_id.name == users[2]:
                i.discount_qty = 14
            if self.user_id.name == users[3]:
                i.discount_qty = 16


    def action_validate(self):
     pass
  
    def action_confirmed(self):
        for i in self:
            i.state='manager'

    def action_done(self):
        for i in self:
            i.state='director'

    @api.onchange("name")
    def onchange_partner_id(self):
        self.address=self.name.street

    @api.depends("request_line.total")
    def compute_total_invoice(self):
        total = 0
        for i in self.request_line:
            total= total + i.total
        self.update({
            'net_total': total})


class ReturnRequested(models.Model):
    _name = 'request.line'
    _description='Return Request Line'

    request_order_line = fields.Many2one("returns.bash")
    invoice_dte = fields.Date("Invoice Date", related = 'invoice_no.date_invoice')
    invoice_no = fields.Many2one("account.invoice")
    item_description = fields.Many2one("product.product", string="Item Description")
    art = fields.Char("Art")
    sold_quantity = fields.Integer("Sold Qty")
    previous_return_quantity = fields.Integer("Previous Return Qty")
    return_quantity = fields.Integer("Return Qty")
    discount_qty = fields.Float("Discount")
    res_qty = fields.Float(string="Reserved Quantity")
    on_hand = fields.Float("On Hand")
    unit_price = fields.Float("Unit Price")
    total = fields.Float("Total", compute= "compute_discount")
    reason_of_return = fields.Char("Reason Of Return")

    @api.onchange('invoice_no')
    def onchange_invoice_id(self):
        invoice_obj = self.env['account.invoice'].search([('partner_id', '=', self.request_order_line.name.id)])
        return {'domain': {'invoice_no': [('id', 'in', invoice_obj.ids)]}}


    #Fetching
    @api.onchange('invoice_no')
    def onchange_get_products(self):
        product_list = []
        for rec in self.invoice_no.invoice_line_ids:
            product_list.append(rec.product_id.id)
        # print("product", product_list)
        return {'domain': {'item_description': [('id', 'in', product_list)]}}



    @api.onchange('item_description')
    def onchange_onhand(self):
        for rec in self:
            self.on_hand = rec.item_description.qty_available


    @api.onchange('item_description')
    def onchange_reserve(self):
        count = 0
        for res in self:
            reserve_qty = self.env['stock.quant'].search([('product_id', '=', res.item_description.id)])
            for obj in reserve_qty:
                count = count+1
                res.res_qty += obj.reserved_quantity



    # Fetching product vs invoices we choose
    @api.onchange('item_description')
    def onchange_item_description(self):
        product_ids = self.env['account.invoice.line'].search(
            [('product_id', '=', self.item_description.id), ('invoice_id', '=', self.invoice_no.id)], limit=1)
        if product_ids:
            self.sold_quantity = product_ids.quantity
            self.unit_price = product_ids.price_unit


    @api.depends("return_quantity","discount_qty")
    def compute_discount(self):
        for rec in self:
            total_object = rec.unit_price * rec.return_quantity
            if rec.discount_qty:
                discount_object = (total_object * rec.discount_qty) / 100
            else:
                discount_object = (total_object * 0) / 100
            rec.total = total_object - discount_object


















