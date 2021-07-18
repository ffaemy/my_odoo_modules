
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseTaxWizard(models.TransientModel):
    _name = 'purchase.tax.wizard'

    tax_ids = fields.Many2many('account.tax')

    def create_taxes(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        for line in rec_model.order_line:
            line.taxes_id = self.tax_ids