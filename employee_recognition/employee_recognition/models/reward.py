from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class EmployeeReward(models.Model):
    _name = 'employee.reward'
    _description = 'Employee Reward'

    name = fields.Char(string='Reward Name', required=True)
    required_points = fields.Integer(string='Required Points', required=True)
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
    )
    state = fields.Selection([
        ('pending', 'Pending'),
        ('redeemed', 'Redeemed')
    ], string='State', default='pending', required=True)
    date_redeemed = fields.Date(string='Date Redeemed')

    @api.constrains('required_points')
    def _check_required_points(self):
        for record in self:
            if record.required_points <= 0:
                raise ValidationError("Required points must be greater than zero.")

    def redeem_reward(self):
        for reward in self:
            print(f"Attempting to redeem reward: {reward.name} for employee: {reward.employee_id.name}")
            
            # Ensure the employee has sufficient points
            total_points = sum(reward.employee_id.achievement_ids.filtered(lambda a: a.state == 'approved').mapped('points'))
            print(f"Total points for {reward.employee_id.name}: {total_points}")

            if total_points < reward.required_points:
                _logger.warning(f"Insufficient points: {total_points} available, {reward.required_points} required")
                raise ValidationError(f"Insufficient points. {reward.employee_id.name} has only {total_points} points.")

            # Deduct the points from the total
            remaining_points = total_points - reward.required_points
            print(f"Remaining points after redemption: {remaining_points}")

            # Update reward state
            reward.write({
                'state': 'redeemed',
                'date_redeemed': fields.Date.today()
            })
            print(f"Reward {reward.name} redeemed successfully for {reward.employee_id.name}")

            return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success!'),
                        'message': _('Reward "%s" has been successfully redeemed. Remaining points after redemption: %s') % (reward.name, total_points - reward.required_points),
                        'type': 'success',
                        'sticky': False,
                    }
                }

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    achievement_ids = fields.One2many(
        'employee.achievement', 
        'employee_id', 
        string='Achievements'
    )
