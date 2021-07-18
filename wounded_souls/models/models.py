# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class wounded_souls_userid(models.Model):
     _inherit = 'res.users'

     allowed_discount = fields.Float("Allowed Discount")


class wounded_souls(models.Model):
    _inherit = 'sale.order'

    contact_person = fields.Many2one("res.partner", string="Contact Person")
    article_no = fields.Char(string="Article No")

    # inv_paid_status = fields.Selection([
    #     ('yes', 'Yes'),
    #     ('no', 'No'),
    #     ])

    today_date= fields.Date(string="Today's Date", default=date.today() )

    @api.constrains('today_date')
    def conf_date_const(self):
            if self.today_date != date.today():
                raise ValidationError("Your date is not correct, It has to be Today.s Date")



    # def invoice_status_obj(self):
    #     inv_sta_obj = self.env['account.invoice'].search([('origin', '=', self.name)])
    #     if inv_sta_obj.state == 'paid':
    #         self.inv_paid_status = 'yes'
    # else:
    #         self.inv_paid_status = 'no'


class wounded_souls_saleorder(models.Model):
    _inherit = 'sale.order.line'

    article_noo = fields.Char(string="Article No", related='order_id.article_no')



class wounded_souls(models.Model):
    _name = 'wounded.souls'
    _rec_name = "customer"

    @api.depends('order_line.sub_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = 0.0

            for line in order.order_line:
                amount_untaxed += line.sub_total
            order.update({
                'total': amount_untaxed
            })

    @api.depends('order_line.item_quantity')
    def get_quantity_sum(self):
        for qty in self:
            total_quantity = 0.0
            print(total_quantity)
            print()

            for line in qty.order_line:
                total_quantity = total_quantity + line.item_quantity
            qty.update({
                'qty_sum': total_quantity
            })


    allowed_discount = fields.Float("Allowed Discount", related='user_id.allowed_discount',store='True')
    max_discount = fields.Float("Maximum Discount")
    name_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    order_line = fields.One2many('wounded.souls.orderline','order_id', string='Order Lines')

    item_no = fields.Char("Product No")
    order_no = fields.Char(string='Order Number', related='name_seq')
    address = fields.Char("Invoice Address")

    @api.onchange('customer')
    def onchange_address(self):
        self.address = self.customer.street

    customer = fields.Many2one("res.partner", string='Customer')
    customer_ref = fields.Char("Customer Reference")

    @api.onchange("customer")
    def onchange_customer(self):
        self.customer_ref = self.customer.ref

    confirmation_date = fields.Datetime(string='Confirmation Date')

    payment_term=fields.Selection([
        ('immediate','Immediate Payment'),
        ('15days','15 Days'),
        ('15days', '15 Days'),
        ('30net', '30 Net Days'),
        ('2month', '2 Months'),
        ('endofnext', 'End of Next Month'),
        ('30%', '30% Advance End of Following Month'),
        ], string="Payment Term", default='immediate')

    name = fields.Many2one("product.product", string="Add Product Name")
    description = fields.Char("Description")


    #sale_obj = fields.Many2one("sale.order", string="Sale Order")
    #wh_out = fields.Many2one("stock.picking", string="WH Out")
    #sale_address = fields.Many2one(string="Customer Reference", related='sale_obj.partner_id')

    user_id = fields.Many2one('res.users', string='User', default=lambda self:self.env.user, readonly=True)

    quantity = fields.Integer("Available Qty")
    qty_sum = fields.Integer("Qty Sum", compute="get_quantity_sum")
    unit_price = fields.Float("Unit Price")
    sell_price = fields.Float("Selling Price")
    sub_total = fields.Many2one("wounded.souls.orderline","Sub Total")
    total = fields.Float("Total" ,compute ="_amount_all")

    status = fields.Selection([
        ('ebay', 'Ebay Sale'),
        ('web', 'Website'),
        ('amazon', 'Amazon'),
        ],)
    sold_quantities = fields.Integer("Sold Quantity")
    website_item_code = fields.Integer("Website Item Code")
    tags=fields.Many2many("wounded.souls.orderline", string="Product Tags")
    date = fields.Date(string="Entry Date")


    varient = fields.Selection([
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xl1', 'XL1'),
        ('xl2', 'XL2'),
        ('xl3', 'XL3'),
        ('xl4', 'XL4'),
    ], 'Varient', default="s")

    payment_mode = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('debit', 'Visa Debit'),
        ('credit', 'Credit Card'),
        ('master', 'Master Card'),
        ('paypal', 'Paypal'),
    ],)
    del_mode = fields.Selection([
        ('royal', 'Royalmail 2nd Class'),
        ('hermes', 'Hermes'),
        ('royal1', 'Royalmail 1st Class'),
        ('dpd', 'DPD'),
        ('other', 'Other'),
        ('collection', 'Collection'),
    ],)
    #del_country = fields.Char("Delivery Country")
    stock_location = fields.Char("Stock Location")
    barcode = fields.Integer("Barcode")
    state = fields.Selection([
        ('step1', 'Step 1'),
        ('step2', 'Step 2'),
        ('step3', 'Step 3'),

    ], 'Order Status', default="step1", readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('wounded_souls_sequence') or _('New')
        result = super(wounded_souls, self).create(vals)
        return result



    #Define Header Button Functions
    def btn_step2(self):
        #self.description = self.customer.name
        self.state="step2"

    def btn_step3(self):
        self.state="step3"

    def btn_step1(self):
        self.state="step1"

    @api.onchange("name")
    def onchange_product_id(self):
        self.item_no= self.name.default_code

    @api.onchange("partner_id")
    def onchange_article_no(self):
        article_obj = self.env['sale.order'].search([('id','=',self.id)])
        # for ao in article_obj:



    #compute function for max discount field which is showing maximum discount value in order line
    def compute_disc_allowed(self):
        for record in self:
            record.max_discount=max(x.discount for x in record.order_line)


class wounded_souls_orderline(models.Model):
    _name = 'wounded.souls.orderline'
    order_id = fields.Many2one('wounded.souls', string='Order Reference')
    name = fields.Many2one("product.product", string="Add Product Name")
    unit_price = fields.Float("Unit Price")
    sell_price = fields.Float("Selling Price")
    discount = fields.Float("Discount %")


    sub_total = fields.Float("Sub Total", compute="discount_calc")
    def discount_calc(self):
        for rec in self:
            total_o = rec.sell_price * rec.item_quantity
            if total_o:
                discount_obj = (total_o * rec.discount)/100
            else:
                discount_obj = (total_o *0)/100
            rec.total = total_o - discount_obj

                

    item_quantity = fields.Integer("Qty")

    @api.onchange("name")
    def onchange_product_id(self):
        self.sell_price = self.name.list_price

    @api.onchange("item_quantity")
    def subtotal_qty(self):
        self.sub_total= self.item_quantity*self.sell_price


