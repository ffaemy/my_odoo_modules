from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    woo_order_id = fields.Char(string="WooCommerce Order ID", copy=False, index=True)
    woo_order_key = fields.Char(string="WooCommerce Order Key", copy=False)
    woo_status = fields.Char(string="WooCommerce Status", copy=False)
    woo_sync_date = fields.Datetime(string="WooCommerce Last Sync", copy=False)
    woo_booking_service = fields.Char(string="Booking Service", copy=False)
    woo_booking_start = fields.Datetime(string="Booking Start", copy=False)
    woo_booking_stop = fields.Datetime(string="Booking End", copy=False)
    woo_booking_staff = fields.Char(string="Booking Staff", copy=False)
    woo_booking_notes = fields.Text(string="Booking Notes", copy=False)
    woo_calendar_event_id = fields.Many2one(
        "calendar.event",
        string="Calendar Appointment",
        copy=False,
        readonly=True,
    )
