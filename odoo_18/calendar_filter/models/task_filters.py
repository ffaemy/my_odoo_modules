from odoo import fields, models, api, _

class Task(models.Model):
    _inherit = 'project.task'

    assignee_id = fields.Many2one('res.users', string='Assignee', index=True)

class TaskFilters(models.Model):
    _name = 'task.filters'
    _description = 'Task Filters'

    user_id = fields.Many2one('res.users', 'Me', required=True,  index=True, ondelete='cascade')
    assignee_id = fields.Many2one('res.users', 'Assignee', required=True, index=True)
    active = fields.Boolean('Active', default=True)
    assignee_checked = fields.Boolean('Checked', default=True)

    _sql_constraints = [
        ('user_id_assignee_id_unique', 'UNIQUE(user_id, assignee_id)', 'A user cannot have the same assignee twice.')
    ]

    @api.model
    def unlink_from_assignee_id(self, assignee_id):
        return self.search([('assignee_id', '=', assignee_id)]).unlink()