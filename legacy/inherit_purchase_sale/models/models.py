# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class InheritPurchaseSale(models.Model):
    _inherit = 'purchase.order'

    sale_ord = fields.Many2one("sale.order", string="Sale Order")

class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    line_id = fields.Integer(string="Line Id")


    # def line_id_func(self):
    #     count = 0
    #     for res in self:
    #         count = count + 1
    #         res.line_id += count

class InheritSaleOrderLine(models.Model):
    _inherit = 'stock.move'

    sale_line_idd = fields.Integer(string="Line Id", compute="line_idd_func")
    p_order = fields.Many2one("purchase.order", string="Purchase Order", compute="onchange_func")


    # def default_get(self, fields):
    #     res = super(InheritSaleOrderLine, self).default_get(fields)
    #     sale_lines = []
    #     sale_rec = self.env['purchase.order'].search([('sale_ord.name','=',res.picking_id.origin)])
    #     for rec in sale_rec:
    #         self.p_order = rec.id
    #     return res
    @api.depends('product_id')
    def onchange_func(self):
        for k in self:
            sale_rec = self.env['purchase.order'].search([('sale_ord.name', '=', k.picking_id.origin)])
            for i in sale_rec:
                k.p_order = i.id




    # @api.onchange('sale_line_idd')
    # def obj_po(self):
    #     purchase_obj = self.env['purchase.order'].search([('origin', '=', self.origin)])
    #     for i in purchase_obj:
            # print(i)


    @api.depends('partner_id')
    def line_idd_func(self):
        count = 0
        for obj in self:
            count = count + 1
            obj.sale_line_idd += count

    # @api.model
    # def create(self,vals):
    #     vals['line_id']=self.env['ir.sequence'].next_by_code('line.sequence')
    #     result=super(InheritPurchaseOrderLine, self).create(vals)
    #     return result


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    s_order = fields.Integer(string="Line Id")


class sale_line_values(models.Model):
    _inherit = 'sale.order'

    contact_person = fields.Many2one("res.users", string="Responsible")



    def action_values(self):
        line_vals = []
        line_vals.append((0, 0, {
            'product_id': 33,
                'price_unit': 50,
                # 'price_subtotal': line.subtotal,
                # 'tax_ids': line.tax_ids,
                'product_uom_qty': 10,

            }))

        line_vals.append(line_vals)
        #print(line_vals)
        vals = {
            'partner_id': 11,
             'order_line': line_vals,

        }
        move = self.env['sale.order'].create(vals)

    def action_invoice(self):
        line_vals = []
        line_vals.append((0, 0, {
            'product_id': 30,
            'price_unit': 50,
            'name': 'FURN_2333',
                # 'price_subtotal': line.subtotal,
                # 'tax_ids': line.tax_ids,
            'account_id': 17,
            }))

        line_vals.append(line_vals)
        #print(line_vals)
        vals = {
            'partner_id': 4,
             'invoice_line_ids': line_vals,

        }
        move = self.env['account.invoice'].create(vals)