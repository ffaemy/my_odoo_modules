from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MeetingRoomBooking(models.Model):
    _name = 'meeting.booking'
    _description = 'Meeting Room Booking'

    name = fields.Char(string='Booking Reference', required=True, default='New')
    room_id = fields.Many2one('meeting.room', string='Room', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    booked_by = fields.Many2one('res.users', string='Booked By', default=lambda self: self.env.user)

    @api.constrains('start_time', 'end_time', 'room_id')
    def _check_double_booking(self):
        for booking in self:
            overlapping_bookings = self.search([
                ('room_id', '=', booking.room_id.id),
                ('id', '!=', booking.id),
                ('start_time', '<', booking.end_time),
                ('end_time', '>', booking.start_time),
            ])
            if overlapping_bookings:
                raise ValidationError('The selected room is already booked for the specified time.')