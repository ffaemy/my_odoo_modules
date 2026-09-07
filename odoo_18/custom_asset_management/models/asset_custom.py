from odoo import models, fields, api  # Importing Odoo's libraries for model, fields, and decorators.

from odoo.exceptions import ValidationError

class AssetAsset(models.Model):
    _name = 'asset.asset'
    _description = 'Asset'

    name = fields.Char(string='Asset Name', required=True)
    category_id = fields.Many2one(
        'asset.category',
        string='Category',
        required=True,
        default=lambda self: self.env['asset.category'].search([], limit=1)
    )
    value = fields.Float(string='Purchase Value', required=True)
    purchase_date = fields.Date(string='Purchase Date', required=True)
    depreciation_rate = fields.Float(string='Depreciation Rate (%)', required=True)
    employee_id = fields.Many2one(
        'hr.employee',
        string='Assigned To',
        default=lambda self: self.env['hr.employee'].search([], limit=1)
    )
    current_value = fields.Float(string='Current Value', compute='_compute_current_value', store=True)

    @api.depends('value', 'depreciation_rate', 'purchase_date')
    def _compute_current_value(self):
        for record in self:
            if record.purchase_date:
                years = (fields.Date.today() - record.purchase_date).days / 365.0
                record.current_value = record.value * (1 - (record.depreciation_rate / 100) * years)

    @api.constrains('category_id', 'employee_id')
    def _check_m2o_fields(self):
        for record in self:
            if not record.category_id:
                raise ValidationError("Category is required.")
            if not record.employee_id:
                raise ValidationError("Assigned Employee is required.")

