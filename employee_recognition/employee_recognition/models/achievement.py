from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EmployeeAchievement(models.Model):
    _name = 'employee.achievement'
    _description = 'Employee Achievement'

    name = fields.Char(string='Achievement Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    type_id = fields.Many2one(
    'achievement.type',
    string='Achievement Type',
    required=True,
    default=lambda self: self.env['achievement.type'].search([], limit=1)
)

    points = fields.Integer(string='Points', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], string='State', default='draft', required=True)
    date_awarded = fields.Date(string='Date Awarded', default=fields.Date.today, required=True)

   
    
    @api.constrains('points')
    def _check_points(self):
        for record in self:
            if record.points < 0 or record.points > 100:
                raise ValidationError("Points must be between 0 and 100.")

    def approve_achievement(self):
        for record in self:
            if record.state == 'approved':
                raise ValidationError("This achievement is already approved.")
            record.write({'state': 'approved'})

    def reset_to_draft(self):
        for record in self:
            record.write({'state': 'draft'})


class AchievementType(models.Model):
    _name = 'achievement.type'
    _description = 'Achievement Type'

    name = fields.Char(string='Type Name', required=True)
    description = fields.Text(string='Description')
