# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class OdooisticApprovalRule(models.Model):
    _name = "odooistic.approval.rule"
    _description = "Approval Rule (Sale Order)"
    _order = "sequence, min_amount, id"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    sequence = fields.Integer(default=10)
    min_amount = fields.Monetary(string="Minimum Amount", required=True, default=0.0)
    currency_id = fields.Many2one(related="company_id.currency_id", store=True, readonly=True)

    group_id = fields.Many2one(
        "res.groups",
        string="Approver Group",
        required=True,
        help="Users in this group can approve when order total is >= Minimum Amount.",
    )

    @api.constrains("min_amount")
    def _check_min_amount(self):
        for r in self:
            if r.min_amount < 0:
                raise ValidationError("Minimum Amount cannot be negative.")
