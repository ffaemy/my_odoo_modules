from odoo import http, fields
from odoo.http import request


class AppointmentBookingController(http.Controller):
    @http.route("/appointments/book", type="http", auth="public", methods=["GET"], website=True)
    def appointment_form(self, **kwargs):
        return request.render("appointment_booking_widget.appointment_booking_form", {})

    @http.route("/appointments/book", type="http", auth="public", methods=["POST"], website=True, csrf=True)
    def appointment_submit(self, **post):
        preferred_dt = post.get("preferred_datetime")
        if preferred_dt:
            # HTML datetime-local uses "YYYY-MM-DDTHH:MM", replace T to match Odoo format
            preferred_dt = preferred_dt.replace("T", " ")
            if len(preferred_dt) == 16:
                preferred_dt += ":00"
            # standardize using Odoo helpers
            preferred_dt = fields.Datetime.to_string(fields.Datetime.from_string(preferred_dt))
        vals = {
            "partner_name": post.get("partner_name"),
            "partner_email": post.get("partner_email"),
            "phone": post.get("phone"),
            "preferred_datetime": preferred_dt,
            "notes": post.get("notes"),
        }
        request.env["appointment.booking"].sudo().create(vals)
        return request.render("appointment_booking_widget.appointment_booking_thanks", {"partner_name": post.get("partner_name")})
