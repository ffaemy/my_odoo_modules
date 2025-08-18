from odoo import http
from odoo.http import request


class TaskNotificationController(http.Controller):

    @http.route('/task_notification/tasks', type='json', auth='user')
    def get_tasks(self):
        """
        Return the 5 most recent project tasks visible to the current user.
        """
        tasks = request.env['project.task'].search(
            [],
            limit=5,
            order='create_date desc'
        )
        return [
            {
                'id': task.id,
                'name': task.display_name,  # better UX in case name is not set
            }
            for task in tasks
        ]
