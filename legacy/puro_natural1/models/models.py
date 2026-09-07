# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class PureNaturalInv(models.Model):
    _inherit = 'product.product'

    packing = fields.Selection([
        ('sachet', 'SACHET'),
        ('box', 'BOX'),
        ('bottle', 'BOTTLE'),
        ('jar', 'JAR'),
        ('pack', 'PACK'),
        ('glass', 'GLASS'),
        ('dropper', 'DROPPER'),
        ('POUCH', 'POUCH'),
    ], string="Packing", default='pack')

    container_pack = fields.Integer(string="Container Capacity")

    invoice_rate_cotton = fields.Float(string="Inv Rate Per Ctn", compute="inv_rate_cotton")
    def inv_rate_cotton(self):
        for i in self:
            i.invoice_rate_cotton = i.tp_rate_cotton - i.dist_margin_per_ctn

    tp_rate_cotton = fields.Float(string="TP Rate Per Ctn", compute="cotton_rate")
    def cotton_rate(self):
        for rec in self:
            rec.tp_rate_cotton = rec.container_pack * rec.standard_price


    dist_margin_per_unit = fields.Float(string="Dist Margin Per Unit", compute="dist_margin")
    def dist_margin(self):
        for i in self:
            i.dist_margin_per_unit = i.tp_unit_rate - i.lst_price

    dist_margin_per_ctn = fields.Float(string="Dist Margin Per Ctn", compute="dist_margin_ctn")
    def dist_margin_ctn(self):
        for obj in self:
            obj.dist_margin_per_ctn = (obj.tp_rate_cotton * 10.72)/100




    dist_margin_perc = fields.Float(string="Dist Margin in %", compute="margin_perc")
    def margin_perc(self):
        for i in self:
            i.dist_margin_perc = (i.dist_margin_per_unit/i.lst_price)*100

    retail_unit = fields.Float(string="Retail Per Unit")
    tp_unit_rate = fields.Float(string="TP Rate Per Unit")


class PureNaturalInvoice(models.Model):
    _inherit = 'account.invoice.line'

    ctn = fields.Integer(string="Ctn")
    tp_per_cotton = fields.Float(string="TP Rate Per Ctn")
    inv_per_cotton = fields.Float(string="Inv Rate Per Ctn")

    @api.onchange('ctn')
    def ctn_calc(self):
        for i in self:
            i.quantity = i.ctn * i.ctn_packing
            i.tp_per_cotton = i.ctn_packing * i.product_id.tp_unit_rate
            i.inv_per_cotton = i.tp_per_cotton - i.product_id.dist_margin_per_ctn
            i.tp_rate_value = i.ctn * i.tp_per_cotton
            i.dist_marg = (i.ctn * i.inv_per_cotton) * 12 / 100


    ctn_packing = fields.Integer(string="Ctn Packing", related='product_id.container_pack')
    retail_price = fields.Float(string="Retail Price", related='product_id.retail_unit')
    tp_rate_unit = fields.Float(string="TP Rate Per Unit", related='product_id.tp_unit_rate')
    dist_margin_unit = fields.Float(string="Dist Marg Per Unit", related='product_id.dist_margin_per_unit')
    dist_margin_ctn = fields.Float(string="Dist Marg Per Ctn", related='product_id.dist_margin_per_ctn')
    dist_marg_percentage = fields.Float(string="Dist Marg in %", related="product_id.dist_margin_per_ctn")

    tp_rate_value = fields.Float(string="TP Rate in Value")

    dist_marg = fields.Float(string="Dist Margin 12%")




