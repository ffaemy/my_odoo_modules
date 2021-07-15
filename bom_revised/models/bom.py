# -*- coding: utf-8 -*-


import datetime
from odoo import models, fields, api,_
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime



class MrpBomIn(models.Model):
    _inherit = 'mrp.bom'

    comments = fields.Text(string='Comments', tracking=True)
    check = fields.Boolean(string='Check')

    @api.model
    def create(self, vals):
        record = super(MrpBomIn, self).create(vals)
        record.create_revised_bom(vals, record)
        return record

    def write(self, vals):
        record = super(MrpBomIn, self).write(vals)
        if (datetime.now() - self.create_date).days > 7:
            if not self.comments:
                print((datetime.now() - self.create_date).days)
                raise ValidationError(_("Please add comments"))
            else:
                self._update_record()
                return record
        else:
            return record

        

    def _update_record(self):
        line_val = []
        for line in self.bom_line_ids:
            line_val.append((0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'product_uom_id': line.product_uom_id.id,
            }))

        record = self.env['revised.bom'].create({
            'product_tmpl_id': self.product_tmpl_id.id,
            'code': self.code,
            'type': self.type,
            'comments': self.comments,
            'product_id': self.product_id.id,
            'product_qty': self.product_qty,
            'revised_bom_lines': line_val,
        })

    def create_revised_bom(self, vals, record):
            line_vals = []
            print(record)
            for line in vals['bom_line_ids']:
                print(line[2].get('product_id'))
                line_vals.append((0, 0, {
                    'product_id': line[2].get('product_id'),
                    'product_qty': line[2].get('product_qty'),
                    'product_uom_id': line[2].get('product_uom_id'),
                }))
                line_vals.append(line_vals)
            vals = {
                'product_tmpl_id': vals['product_tmpl_id'],
                'bom_id': record.id,
                'product_id': vals['product_id'],
                'code': vals['code'],
                'type': vals['type'],
                'comments': vals['comments'],
                'company_id': vals['company_id'],
                'product_qty': vals['product_qty'],
                'revised_bom_lines': line_vals,
            }
            bom = self.env['revised.bom'].create(vals)


class BomTacking(models.Model):
    _name = 'revised.bom'
    _rec_name = 'product_tmpl_id'

    product_tmpl_id = fields.Many2one('product.template')
    code = fields.Char('Reference')
    type = fields.Selection([('normal', 'Manufacture this product'),('phantom', 'Kit')], string='normal', required=True)

    company_id = fields.Many2one('res.company')
    product_id = fields.Many2one('product.product')
    product_qty = fields.Float('Quantity')
    bom_id = fields.Many2one('mrp.bom')
    revised_bom_lines = fields.One2many('revised.bom.line', 'revised_bom_id')
    comments = fields.Text(string='Comments')
    check = fields.Boolean(string='Check', default=False)

class BomTackingLine(models.Model):
    _name = 'revised.bom.line'

    revised_bom_id = fields.Many2one('revised.bom')
    product_id = fields.Many2one('product.product')
    product_qty = fields.Float('Quantity')
    product_uom_id = fields.Many2one('uom.uom')