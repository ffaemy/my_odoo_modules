# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class EffectiveDate(models.Model):
    _inherit = 'sale.order'

    effective_date = fields.Datetime('Effective Date', compute="compute_effective_date")

    def compute_effective_date(self):
        for i in self:
            obj = self.env['stock.piking'].search([('origin', '=', i.name), ('state', '=', 'done')])
            for k in obj:
                if k.state == "done":
                    if k.picking_type_id.code == "outgoing":
                        i.effective_date = k.date_done
                        break

class ExportTrade(models.Model):
    _inherit = 'spiral.export.report'

    hs_code = fields.Char(string="HS Code", related= 'product_id.hs_code')
    percentage = fields.Integer(string="Percentage")
    stock_field = fields.Float(string="Stock Available", related='product_id.qty_available_not_res')
    country_of_origin = fields.Char(string="Country Of Origin", related='product_id.country_of_origin')

