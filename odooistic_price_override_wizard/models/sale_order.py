# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.tools.float_utils import float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_price_override_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Price Override",
            "res_model": "price.override.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_order_id": self.id,
            },
        }

    @api.model
    def price_override_preview(self, order_id, discount_percent):
        order = self.browse(int(order_id)).exists()
        if not order:
            return {"error": "Sale Order not found."}

        discount = float(discount_percent or 0.0)
        discount = max(0.0, min(100.0, discount))
        factor = 1.0 - (discount / 100.0)

        currency = order.currency_id
        partner = order.partner_shipping_id or order.partner_id

        amount_untaxed = 0.0
        amount_tax = 0.0

        for line in order.order_line.filtered(lambda l: not l.display_type):
            qty = line.product_uom_qty
            unit_price = line.price_unit * factor

            taxes_res = line.tax_ids.compute_all(
                unit_price,
                currency=currency,
                quantity=qty,
                product=line.product_id,
                partner=partner,
            )
            amount_untaxed += taxes_res["total_excluded"]
            amount_tax += taxes_res["total_included"] - taxes_res["total_excluded"]

        amount_untaxed = float_round(amount_untaxed, precision_rounding=currency.rounding)
        amount_tax = float_round(amount_tax, precision_rounding=currency.rounding)
        amount_total = float_round(amount_untaxed + amount_tax, precision_rounding=currency.rounding)

        return {
            "discount_percent": discount,
            "amount_untaxed": amount_untaxed,
            "amount_tax": amount_tax,
            "amount_total": amount_total,
            "currency_symbol": currency.symbol,
            "currency_position": currency.position,
        }

    @api.model
    def price_override_apply_bulk_discount(self, order_id, discount_percent):
        order = self.browse(int(order_id)).exists()
        if not order:
            return {"error": "Sale Order not found."}

        discount = float(discount_percent or 0.0)
        discount = max(0.0, min(100.0, discount))

        lines = order.order_line.filtered(lambda l: not l.display_type)
        lines.write({"discount": discount})

        order._amount_all()
        return {"success": True, "discount_percent": discount}
