# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountInvoice(models.Model):

    _inherit = 'account.move'


    disbatched_by = fields.Many2one('res.partner', "Dispatched by")
    previous_bal = fields.Monetary(string='Previous Balance',compute="_compute_balance")
    closing_bal = fields.Monetary(string='Closing Balance',compute="_compute_balance")


@api.depends("partner_id")


def _compute_balance(self):
    self.previous_bal = 0
    self.closing_bal = 0
    if self.partner_id:
        if not self.state == 'draft':
            self.previous_bal = self.partner_id._get_total_due() or 0.0 - self.amount_total
            self.closing_bal = self.amount_total + self.previous_bal
        else:
            self.previous_bal = self.partner_id._get_total_due() or 0.0
            self.closing_bal = self.amount_total + self.previous_bal


class AccountInvoiceLine(models.Model):

    _inherit = 'account.move.line'


    item_code = fields.Char(string='Item Code')
    sku = fields.Char(string='SKU')
    packing = fields.Char(string='Packing')
    ctn = fields.Integer(string='Ctn')
    ctn_packing = fields.Float(string='Ctn Packing', digits='Product Price')
    tp_unit_ctn_rate = fields.Float(string='T.P Rate Per Ctn', digits='Product Price')
    invoice_rate = fields.Float(string='Invoice Rate Per Unit', digits='Product Price')
    invoice_rate_per_ctn = fields.Float(string='Invoice Rate Per Ctn', digits='Product Price')
    dist_margin_unit = fields.Float(string='Dist Margin Per Unit', digits='Product Price')
    dist_margin_ctn = fields.Float(string='Dist Margin Per Ctn', digits='Product Price')
    dist_margin = fields.Float(string='Dist Margin In %', precision_digits=5)
    retail_price = fields.Float(string='Retail Price Per Unit')
    tp_rate_value = fields.Float(string='T.P Rate in Value', digits='Product Price')
    dist_margin_12 = fields.Float(string='Distributor Margin (12%)', digits='Product Price')
    trade_offer = fields.Many2one('create.offers',string='Trade Offer',related="product_id.trade_offers")
    trade_offer_percent = fields.Float(string="Trade Offer %", related="trade_offer.value")
    trade_offer_amount = fields.Float(string='Trade Offer Amount Rs.',compute="comput_trade_offer_amount")
    retail_price_per_ctn = fields.Float(string='Retail Price Per Ctn', digits='Product Price')
    net_amount = fields.Float(string='Net amount', digits='Product Price')

    @api.depends('tp_rate_value')
    def comput_trade_offer_amount(self):
        for line in self:
            line.trade_offer_amount = ((line.tp_rate_value * line.trade_offer_percent) / 100)
            line.dist_margin_12 = (line.ctn * line.invoice_rate_per_ctn) * 0.120

    @api.onchange('ctn', 'product_id', 'ctn_packing')
    def price_product_change(self):
        for line in self:
            line.ctn_packing = line.product_id.product_packing
            line.update({'quantity': line.ctn * line.ctn_packing})

    @api.onchange('product_id', 'tp_rate_value', 'price_unit', 'dist_margin_unit', 'trade_offer_amount', 'trade_offer',
                  'quantity', 'ctn', 'retail_price_per_ctn', 'dist_margin_ctn', 'ctn_packing', 'dist_margin',
                  'trade_offer_amount')
    def _get_tp_rate_per(self):
        for line in self:
            line.tp_unit_ctn_rate = line.price_unit * line.ctn_packing
            line.dist_margin_unit = line.price_unit * 10.72 / 100
            line.dist_margin_ctn = line.tp_unit_ctn_rate * 10.72 / 100
            line.invoice_rate = line.price_unit - line.dist_margin_unit or 1
            line.dist_margin = line.dist_margin_unit / line.invoice_rate
            line.invoice_rate_per_ctn = line.tp_unit_ctn_rate - line.dist_margin_ctn
            line.tp_rate_value = line.ctn * line.tp_unit_ctn_rate
            line.retail_price = line.product_id.retail_price
            line.retail_price_per_ctn = line.ctn_packing * line.retail_price

    @api.onchange('dist_margin_12', 'trade_offer_amount')
    def _get_net_amount(self):
        for line in self:
            line.net_amount = line.tp_rate_value - (line.dist_margin_12 + line.trade_offer_amount)
            price = line.net_amount / (line.quantity or 1)
            newprice = line.price_unit - price
            line.discount = (newprice / (line.price_unit or 1)) * 100


class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Product Packing')

class EducationHistory(models.Model):
    _inherit = 'product.template'

    product_brand = fields.Many2one("product.brand",'Packing')
    trade_offers = fields.Many2one("create.offers", 'Trade Offers')
    sku = fields.Char(string='Item code')
    product_packing = fields.Float(string='Ctn Packing')
    retail_price = fields.Float(string='Retail Price')