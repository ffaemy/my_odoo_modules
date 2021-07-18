from odoo import api, fields, models
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def _get_total_due(self):
        today = fields.Date.context_today(self)
        aml_obj = self.env['account.move.line']
        for record in self:
            total_due = 0
            amls = aml_obj.search([('partner_id','=', record.id), ('reconciled', '=', False),('account_id.deprecated', '=', False),('account_id.internal_type', '=', 'receivable')])
            for aml in amls:
                if aml.company_id == self.env.company:
                    total_due += aml.amount_residual
            return total_due

class StockMove(models.Model):

    _inherit = 'stock.picking'

    freight_amount = fields.Float(string='Freight Amount')

class StockMove(models.Model):

    _inherit = 'stock.move'

    ctn = fields.Float(string='Ctn' )
    ctn_packing = fields.Float(string='Ctn Packing' )

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        qty = 0.0
        for so in self:
            for line in so.order_line:
                stock_move = self.env['stock.move'].search([('origin', '=', self.name)])
                stock_move.quantity_done = line.product_uom_qty
                stock_move.ctn = line.ctn
                stock_move.ctn_packing = line.ctn_packing
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'


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
            line.dist_margin_12 = (line.ctn * line.invoice_rate_per_ctn)*0.120
    @api.onchange('ctn','product_id','ctn_packing')
    def  price_product_change(self):
        for line in self:
            line.ctn_packing = line.product_id.product_packing
            line.update({'product_uom_qty':line.ctn * line.ctn_packing})

    @api.onchange('product_id','tp_rate_value','price_unit','dist_margin_unit','trade_offer_amount' ,'trade_offer','product_uom_qty', 'ctn','retail_price_per_ctn', 'dist_margin_ctn','ctn_packing', 'dist_margin','trade_offer_amount')
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

    @api.onchange('dist_margin_12','trade_offer_amount')
    def _get_net_amount(self):
        for line in self:
            line.net_amount = line.tp_rate_value - (line.dist_margin_12 + line.trade_offer_amount)
            price = line.net_amount / (line.product_uom_qty or 1)
            newprice = line.price_unit - price
            line.discount = (newprice / (line.price_unit or 1)) * 100

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'ctn': self.ctn, 'ctn_packing': self.ctn_packing,
                    'retail_price': self.retail_price,
                    'tp_unit_ctn_rate': self.tp_unit_ctn_rate,
                    'trade_offer_amount': self.trade_offer_amount,
                    'trade_offer_percent': self.trade_offer_percent,
                    'trade_offer': self.trade_offer,
                    'dist_margin_12': self.dist_margin_12,
                    'tp_rate_value': self.tp_rate_value ,
                    'dist_margin': self.dist_margin,
                    'dist_margin_ctn': self.dist_margin_ctn,
                    'dist_margin_unit': self.dist_margin_unit,
                    'invoice_rate_per_ctn': self.invoice_rate_per_ctn,
                    'invoice_rate': self.invoice_rate})
        return res


class TradeOffers(models.Model):
    _name = 'create.offers'

    name = fields.Char(string="Trade Offer")
    value = fields.Float(string="Trade Offer %")