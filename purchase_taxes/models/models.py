# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    def action_open_taxes_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apply Taxes',
            'view_id': self.env.ref('purchase_taxes.view_purchase_tax_wizard_form', False).id,
            'target': 'new',
            'res_model': 'purchase.tax.wizard',
            'view_mode': 'form',
        }