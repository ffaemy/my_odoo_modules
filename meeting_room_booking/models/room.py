from odoo import models, fields

class MeetingRoom(models.Model):
    _name = 'meeting.room'
    _description = 'Meeting Room'

    name = fields.Char(string='Room Name', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    location = fields.Char(string='Location')
    availability = fields.Boolean(string='Available', default=True)