from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AppointmentBooking(models.Model):
    _name = "appointment.booking"
    _description = "Website Appointment Booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        tracking=True,
    )
    partner_name = fields.Char(string="Name", required=True, tracking=True)
    partner_email = fields.Char(string="Email", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)
    preferred_datetime = fields.Datetime(string="Preferred Date/Time", tracking=True)
    notes = fields.Text(string="Notes")
    state = fields.Selection(
        [
            ("submitted", "Submitted"),
            ("confirmed", "Confirmed"),
            ("declined", "Declined"),
        ],
        default="submitted",
        tracking=True,
    )
    confirmed_by = fields.Many2one("res.users", string="Confirmed/Declined By", tracking=True, readonly=True)
    decision_note = fields.Text(string="Decision Note")

    @api.model
    def create(self, vals_list):
        # Odoo 17+ passes a list of dicts; accept dict for convenience too.
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("appointment.booking") or _("New")

        records = super().create(vals_list)
        template = self.env.ref("appointment_booking_widget.appointment_booking_email", raise_if_not_found=False)
        if template:
            for record in records:
                if record.partner_email:
                    template.send_mail(record.id, force_send=True, email_values={"email_to": record.partner_email})
        return records

    def action_confirm(self):
        for record in self:
            record.write(
                {
                    "state": "confirmed",
                    "confirmed_by": self.env.user.id,
                }
            )

    def action_decline(self):
        for record in self:
            if not record.decision_note:
                raise ValidationError(_("Please provide a reason in the Decision Note before declining."))
            record.write(
                {
                    "state": "declined",
                    "confirmed_by": self.env.user.id,
                }
            )
