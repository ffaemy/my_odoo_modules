# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    approval_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("to_approve", "Waiting Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        tracking=True,
        copy=False,
    )

    approval_done_rule_ids = fields.Many2many(
        "odooistic.approval.rule",
        string="Completed Approvals",
        copy=False,
    )

    approval_next_group_id = fields.Many2one(
        "res.groups",
        string="Next Approver Group",
        compute="_compute_next_approver_group",
        store=False,
    )

    def _get_applicable_rules(self):
        self.ensure_one()
        rules = self.env["odooistic.approval.rule"].search([
            ("company_id", "=", self.company_id.id),
            ("active", "=", True),
        ], order="sequence asc, min_amount asc, id asc")
        return rules.filtered(lambda r: self.amount_total >= r.min_amount)

    @api.depends("approval_done_rule_ids", "amount_total", "company_id", "approval_state")
    def _compute_next_approver_group(self):
        for order in self:
            if order.approval_state != "to_approve":
                order.approval_next_group_id = False
                continue
            pending = order._get_applicable_rules() - order.approval_done_rule_ids
            pending_sorted = pending.sorted(key=lambda r: (r.sequence, r.min_amount, r.id))
            order.approval_next_group_id = pending_sorted[0].group_id if pending_sorted else False

    def action_submit_for_approval(self):
        for order in self:
            if order.state not in ("draft", "sent"):
                raise UserError(_("Only quotations can be submitted for approval."))
            applicable = order._get_applicable_rules()
            order.approval_done_rule_ids = [(5, 0, 0)]
            if not applicable:
                order.approval_state = "approved"
                order.message_post(body=_("No approvals required. Marked as Approved."))
            else:
                order.approval_state = "to_approve"
                order.message_post(body=_("Submitted for approval."))
        return True

    def action_approve(self):
        for order in self:
            if order.approval_state != "to_approve":
                raise UserError(_("This order is not waiting for approval."))
            pending = order._get_applicable_rules() - order.approval_done_rule_ids
            if not pending:
                order.approval_state = "approved"
                return True

            pending_sorted = pending.sorted(key=lambda r: (r.sequence, r.min_amount, r.id))
            next_rule = pending_sorted[0]

            if next_rule.group_id not in self.env.user.all_group_ids:
                raise UserError(_("You are not allowed to approve this step. Required group: %s") % next_rule.group_id.display_name)

            order.approval_done_rule_ids = [(4, next_rule.id)]
            order.message_post(body=_("Approval granted (%s).") % next_rule.name)

            pending2 = order._get_applicable_rules() - order.approval_done_rule_ids
            order.approval_state = "approved" if not pending2 else "to_approve"
        return True

    def action_reject(self):
        for order in self:
            if order.approval_state not in ("to_approve", "approved"):
                raise UserError(_("Only orders waiting approval or approved can be rejected."))
            order.approval_state = "rejected"
            order.message_post(body=_("Order rejected."))
        return True

    def action_reset_approval(self):
        for order in self:
            order.approval_state = "draft"
            order.approval_done_rule_ids = [(5, 0, 0)]
            order.message_post(body=_("Approval reset to Draft."))
        return True

    def action_confirm(self):
        for order in self:
            if order.approval_state in ("to_approve", "rejected"):
                raise UserError(_("You cannot confirm this order until it is Approved."))
            if order.approval_state == "draft" and order._get_applicable_rules():
                raise UserError(_("This order requires approval. Click 'Submit for Approval' first."))
        return super().action_confirm()
