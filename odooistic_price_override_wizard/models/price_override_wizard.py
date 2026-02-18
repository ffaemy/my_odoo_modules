# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class PriceOverrideWizard(models.TransientModel):
    _name = "price.override.wizard"
    _description = "Price Override Wizard"

    order_id = fields.Many2one("sale.order", required=True, readonly=True)
    discount_percent = fields.Float(string="Discount %", default=10.0, required=True)
    currency_id = fields.Many2one("res.currency", related="order_id.currency_id", readonly=True)
    amount_untaxed = fields.Monetary(compute="_compute_preview", currency_field="currency_id", readonly=True)
    amount_tax = fields.Monetary(compute="_compute_preview", currency_field="currency_id", readonly=True)
    amount_total = fields.Monetary(compute="_compute_preview", currency_field="currency_id", readonly=True)

    @api.depends("discount_percent", "order_id", "order_id.order_line", "order_id.order_line.price_unit", "order_id.order_line.product_uom_qty", "order_id.order_line.tax_ids")
    def _compute_preview(self):
        for wizard in self:
            order = wizard.order_id
            if not order:
                wizard.amount_untaxed = 0.0
                wizard.amount_tax = 0.0
                wizard.amount_total = 0.0
                continue

            discount = max(0.0, min(100.0, wizard.discount_percent or 0.0))
            factor = 1.0 - (discount / 100.0)
            currency = order.currency_id
            partner = order.partner_shipping_id or order.partner_id

            amount_untaxed = 0.0
            amount_tax = 0.0
            for line in order.order_line.filtered(lambda l: not l.display_type):
                unit_price = line.price_unit * factor
                taxes_res = line.tax_ids.compute_all(
                    unit_price,
                    currency=currency,
                    quantity=line.product_uom_qty,
                    product=line.product_id,
                    partner=partner,
                )
                amount_untaxed += taxes_res["total_excluded"]
                amount_tax += taxes_res["total_included"] - taxes_res["total_excluded"]

            wizard.amount_untaxed = float_round(amount_untaxed, precision_rounding=currency.rounding)
            wizard.amount_tax = float_round(amount_tax, precision_rounding=currency.rounding)
            wizard.amount_total = float_round(wizard.amount_untaxed + wizard.amount_tax, precision_rounding=currency.rounding)

    def action_apply(self):
        self.ensure_one()
        discount = max(0.0, min(100.0, self.discount_percent or 0.0))
        lines = self.order_id.order_line.filtered(lambda l: not l.display_type)
        lines.write({"discount": discount})
        return {"type": "ir.actions.client", "tag": "reload"}
