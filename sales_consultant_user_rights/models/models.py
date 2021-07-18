# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
from dateutil.relativedelta import relativedelta


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner')
    is_same_branch = fields.Boolean(compute='compute_is_same_branch')


    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('my_branch'):
            args += [('branch_id', '!=', False),
                     ('branch_id', 'in', [branch.id for branch in self.env.user.branch_ids])]
        return super(ResPartnerInh, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                 access_rights_uid=access_rights_uid)

    def compute_is_same_branch(self):

        for rec in self:
            print()
            if rec.branch_id.id == rec.env.user.branch_id.id:
                rec.is_same_branch = True
            else:
                rec.is_same_branch = False

    @api.onchange('user_id')
    def onchange_partner_id(self):
        for rec in self:
            partner = self.env['res.partner'].search([('name', '=', rec.user_id.name)], limit=1)
            rec.partner_id = partner.id


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
        # result = fields_view_get_extra(self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        result = super(ProductTemplateInh, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if self.env.user.has_group('sales_consultant_user_rights.group_readonly_user'):
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('edit', '0')
            result['arch'] = etree.tostring(temp)

        return result


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    is_reserve_approved = fields.Boolean(default=False)
    is_notified = fields.Boolean(default=False)
    is_sent_for_approval = fields.Boolean(default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('manager_approval', 'Approval from Manager'),
        ('ceo_approval', 'Approval from CEO'),
        ('reserve_manager_approvals', 'Reserve Approval from Manager'),
        ('reserve_ceo_approval', 'Reserve Approval from CEO'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(StockPickingInh, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if not self.env.user.has_group('sales_consultant_user_rights.group_show_do_buttons_user'):
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('duplicate', '0')
            temp.set('delete', '0')
            temp.set('edit', '0')
            result['arch'] = etree.tostring(temp)
        if self.env.user.has_group('sales_consultant_user_rights.group_readonly_user'):
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('edit', '0')
            result['arch'] = etree.tostring(temp)

        return result

    def check_date(self):
        transfers = self.env['stock.picking'].search([('state', 'in', ['assigned'])])
        for rec in transfers:
            if rec.scheduled_date:
                diff = datetime.today() - rec.scheduled_date
                if abs(diff.days) > 25:
                    rec._create_notification()
                    rec.is_notified = True
                if abs(diff.days) >= 30:
                    if rec.is_reserve_approved:
                        rec.scheduled_date = rec.scheduled_date + relativedelta(days=15)
                    else:
                        rec.do_unreserve()

    def _create_notification(self):
        # groupObj = self.env['res.groups'].search([('name', '=', "Administrator")])
        # user_list = []
        # for user in groupObj.users:
        #     user_list.append(user.id)
        # if self.sale_id.user_id.id not in user_list:
        #     if self.sale_id.user_id.id:
        #         user_list.append(self.sale_id.user_id.id)
        # for i in user_list:
        #     userObj = self.env['res.users'].browse([i])
        act_type_xmlid = 'mail.mail_activity_data_todo'
        summary = 'Reserved DO Notification'
        note = '25 Days passed.In 5 days left DO will be unreserved Automatically.'
        if act_type_xmlid:
            activity_type = self.sudo().env.ref(act_type_xmlid)
        model_id = self.env['ir.model']._get(self._name).id
        create_vals = {
            'activity_type_id': activity_type.id,
            'summary': summary or activity_type.summary,
            'automated': True,
            'note': note,
            'date_deadline': datetime.today(),
            'res_model_id': model_id,
            'res_id': self.id,
            'user_id': self.sale_id.user_id.id,
        }
        activities = self.env['mail.activity'].create(create_vals)

    def action_reserve_approval_manager(self):
        self.state = 'reserve_ceo_approval'

    def action_reserve_approval_ceo(self):
        for rec in self:
            rec.is_reserve_approved = True
            rec.state = 'assigned'

    def action_send_for_approvals(self):
        for rec in self:
            rec.is_sent_for_approval = True
            rec.state = 'reserve_manager_approvals'


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(AccountMoveInh, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if self.env.user.has_group('sales_consultant_user_rights.group_show_invoice_buttons_user'):
            pass
        else:
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('duplicate', '0')
            temp.set('delete', '0')
            temp.set('edit', '0')
            result['arch'] = etree.tostring(temp)
        return result

