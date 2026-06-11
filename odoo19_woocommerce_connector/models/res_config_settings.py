import logging
import re
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo
from urllib.parse import urljoin

import requests
from dateutil import parser

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    SALON_SERVICE_NAMES = {
        "5574": "Manicure",
    }

    woo_url = fields.Char(
        string="WooCommerce Store URL",
        config_parameter="odoo19_woocommerce_connector.woo_url",
        help="Example: https://your-domain.com",
    )
    woo_consumer_key = fields.Char(
        string="Consumer Key",
        config_parameter="odoo19_woocommerce_connector.consumer_key",
    )
    woo_consumer_secret = fields.Char(
        string="Consumer Secret",
        config_parameter="odoo19_woocommerce_connector.consumer_secret",
    )
    woo_verify_ssl = fields.Boolean(
        string="Verify SSL Certificate",
        default=True,
        config_parameter="odoo19_woocommerce_connector.verify_ssl",
    )
    woo_timeout = fields.Integer(
        string="Request Timeout (seconds)",
        default=30,
        config_parameter="odoo19_woocommerce_connector.timeout",
    )
    woo_import_limit = fields.Integer(
        string="Import Limit",
        default=20,
        config_parameter="odoo19_woocommerce_connector.import_limit",
        help="Maximum records to import per click for tutorial/demo usage.",
    )
    woo_import_statuses = fields.Char(
        string="Order Statuses",
        default="processing,completed,on-hold",
        config_parameter="odoo19_woocommerce_connector.import_statuses",
        help="Comma-separated WooCommerce order statuses to import.",
    )
    woo_create_sale_order = fields.Boolean(
        string="Create Draft Sale Order",
        default=True,
        config_parameter="odoo19_woocommerce_connector.create_sale_order",
    )
    woo_create_calendar_event = fields.Boolean(
        string="Create Calendar Appointment",
        default=True,
        config_parameter="odoo19_woocommerce_connector.create_calendar_event",
    )
    woo_default_booking_duration = fields.Float(
        string="Default Booking Duration",
        default=1.0,
        config_parameter="odoo19_woocommerce_connector.default_booking_duration",
        help="Used when WooCommerce booking metadata has a start time but no end time.",
    )
    salon_api_url = fields.Char(
        string="Salon API URL",
        config_parameter="odoo19_woocommerce_connector.salon_api_url",
        help="Example: https://ifairbeautyandhair.com",
    )
    salon_api_token = fields.Char(
        string="Salon API Token",
        config_parameter="odoo19_woocommerce_connector.salon_api_token",
    )

    # ---------------------------------------------------------------------
    # Configuration helpers
    # ---------------------------------------------------------------------

    def _get_woo_config(self):
        ICP = self.env["ir.config_parameter"].sudo()
        url = (ICP.get_param("odoo19_woocommerce_connector.woo_url") or "").strip().rstrip("/")
        consumer_key = (ICP.get_param("odoo19_woocommerce_connector.consumer_key") or "").strip()
        consumer_secret = (ICP.get_param("odoo19_woocommerce_connector.consumer_secret") or "").strip()
        verify_ssl = ICP.get_param("odoo19_woocommerce_connector.verify_ssl", "True") in ("True", "true", "1")
        default_booking_duration = float(
            ICP.get_param("odoo19_woocommerce_connector.default_booking_duration", "1.0") or 1.0
        )
        timeout = int(ICP.get_param("odoo19_woocommerce_connector.timeout", "30") or 30)
        limit = int(ICP.get_param("odoo19_woocommerce_connector.import_limit", "20") or 20)
        statuses = ICP.get_param(
            "odoo19_woocommerce_connector.import_statuses",
            "processing,completed,on-hold",
        )
        create_sale_order = ICP.get_param(
            "odoo19_woocommerce_connector.create_sale_order",
            "True",
        ) in ("True", "true", "1")
        create_calendar_event = ICP.get_param(
            "odoo19_woocommerce_connector.create_calendar_event",
            "True",
        ) in ("True", "true", "1")
        default_booking_duration = float(
            ICP.get_param("odoo19_woocommerce_connector.default_booking_duration", "1.0") or 1.0
        )

        if not url or not consumer_key or not consumer_secret:
            raise UserError(_("Please configure WooCommerce Store URL, Consumer Key and Consumer Secret first."))

        return {
            "url": url,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "verify_ssl": verify_ssl,
            "timeout": timeout,
            "limit": limit,
            "statuses": [status.strip() for status in statuses.split(",") if status.strip()],
            "create_sale_order": create_sale_order,
            "create_calendar_event": create_calendar_event,
            "default_booking_duration": default_booking_duration,
        }

    def _woo_request(self, endpoint, method="GET", params=None, payload=None):
        config = self._get_woo_config()
        endpoint = endpoint.lstrip("/")
        api_url = urljoin(config["url"] + "/", "wp-json/wc/v3/" + endpoint)
        params = dict(params or {})
        params.update({
            "consumer_key": config["consumer_key"],
            "consumer_secret": config["consumer_secret"],
        })

        try:
            response = requests.request(
                method=method,
                url=api_url,
                params=params,
                json=payload,
                timeout=config["timeout"],
                verify=config["verify_ssl"],
            )
        except requests.exceptions.RequestException as exc:
            raise UserError(_("WooCommerce connection failed:\n%s") % exc) from exc

        if response.status_code not in (200, 201):
            error_text = response.text[:1000]
            raise UserError(_("WooCommerce API error (%s):\n%s") % (response.status_code, error_text))

        try:
            return response.json()
        except ValueError as exc:
            raise UserError(_("WooCommerce returned an invalid JSON response.")) from exc

    def _get_salon_config(self):
        ICP = self.env["ir.config_parameter"].sudo()
        url = (
            ICP.get_param("odoo19_woocommerce_connector.salon_api_url")
            or ICP.get_param("odoo19_woocommerce_connector.woo_url")
            or ""
        ).strip().rstrip("/")
        token = (ICP.get_param("odoo19_woocommerce_connector.salon_api_token") or "").strip()
        timeout = int(ICP.get_param("odoo19_woocommerce_connector.timeout", "30") or 30)
        limit = int(ICP.get_param("odoo19_woocommerce_connector.import_limit", "20") or 20)
        verify_ssl = ICP.get_param("odoo19_woocommerce_connector.verify_ssl", "True") in ("True", "true", "1")
        default_booking_duration = float(
            ICP.get_param("odoo19_woocommerce_connector.default_booking_duration", "1.0") or 1.0
        )

        if not url or not token:
            raise UserError(_("Please configure Salon API URL and Salon API Token first."))

        return {
            "url": url,
            "token": token,
            "timeout": timeout,
            "limit": limit,
            "verify_ssl": verify_ssl,
            "default_booking_duration": default_booking_duration,
        }

    def _salon_request(self, endpoint, params=None):
        config = self._get_salon_config()
        api_url = urljoin(config["url"] + "/", "wp-json/odoo-salon/v3/" + endpoint.lstrip("/"))
        params = dict(params or {})
        params["token"] = config["token"]

        try:
            response = requests.get(
                api_url,
                params=params,
                timeout=config["timeout"],
                verify=config["verify_ssl"],
            )
        except requests.exceptions.RequestException as exc:
            raise UserError(_("Salon API connection failed:\n%s") % exc) from exc

        if response.status_code != 200:
            raise UserError(_("Salon API error (%s):\n%s") % (response.status_code, response.text[:1000]))

        try:
            return response.json()
        except ValueError as exc:
            raise UserError(_("Salon API returned an invalid JSON response.")) from exc

    def _show_notification(self, title, message, notification_type="success"):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": notification_type,
                "sticky": False,
            },
        }

    # ---------------------------------------------------------------------
    # Button actions
    # ---------------------------------------------------------------------

    def action_test_woocommerce_connection(self):
        self.ensure_one()
        products = self._woo_request("products", params={"per_page": 1})
        return self._show_notification(
            _("WooCommerce Connected"),
            _("Connection successful. Odoo can communicate with WooCommerce. Sample products received: %s") % len(products),
        )

    def action_test_salon_connection(self):
        self.ensure_one()
        response = self._salon_request("health")
        return self._show_notification(
            _("Salon API Connected"),
            _("Connection successful. WordPress site replied: %s") % response.get("site", _("OK")),
        )

    def action_import_woo_products(self):
        self.ensure_one()
        config = self._get_woo_config()
        products = self._woo_request("products", params={"per_page": min(config["limit"], 100), "page": 1})
        count = 0
        Product = self.env["product.template"].sudo()

        for item in products:
            woo_id = str(item.get("id"))
            sku = item.get("sku") or ""
            name = item.get("name") or _("WooCommerce Product")
            price = item.get("regular_price") or item.get("price") or 0.0

            product = Product.search([("woo_id", "=", woo_id)], limit=1)
            if not product and sku:
                product = Product.search([("default_code", "=", sku)], limit=1)

            vals = {
                "name": name,
                "woo_id": woo_id,
                "woo_sku": sku,
                "default_code": sku or False,
                "list_price": float(price or 0.0),
                "description_sale": item.get("short_description") or item.get("description") or False,
                "woo_sync_date": fields.Datetime.now(),
            }
            if product:
                product.write(vals)
            else:
                vals.update({"sale_ok": True, "purchase_ok": False})
                Product.create(vals)
            count += 1

        return self._show_notification(_("Products Imported"), _("Imported/updated %s WooCommerce products.") % count)

    def action_import_woo_customers(self):
        self.ensure_one()
        config = self._get_woo_config()
        customers = self._woo_request("customers", params={"per_page": min(config["limit"], 100), "page": 1})
        count = 0
        Partner = self.env["res.partner"].sudo()

        for item in customers:
            woo_id = str(item.get("id"))
            email = item.get("email") or ""
            first_name = item.get("first_name") or ""
            last_name = item.get("last_name") or ""
            billing = item.get("billing") or {}
            name = (first_name + " " + last_name).strip() or billing.get("company") or email or _("WooCommerce Customer")

            partner = Partner.search([("woo_id", "=", woo_id)], limit=1)
            if not partner and email:
                partner = Partner.search([("email", "=", email)], limit=1)

            vals = {
                "name": name,
                "woo_id": woo_id,
                "email": email or False,
                "phone": billing.get("phone") or False,
                "street": billing.get("address_1") or False,
                "street2": billing.get("address_2") or False,
                "city": billing.get("city") or False,
                "zip": billing.get("postcode") or False,
                "woo_sync_date": fields.Datetime.now(),
            }
            if partner:
                partner.write(vals)
            else:
                Partner.create(vals)
            count += 1

        return self._show_notification(_("Customers Imported"), _("Imported/updated %s WooCommerce customers.") % count)

    def action_import_woo_orders(self):
        self.ensure_one()
        config = self._get_woo_config()
        params = {"per_page": min(config["limit"], 100), "page": 1, "orderby": "date", "order": "desc"}
        if config["statuses"]:
            params["status"] = ",".join(config["statuses"])
        orders = self._woo_request("orders", params=params)
        sale_count = 0
        appointment_count = 0
        skipped_count = 0
        SaleOrder = self.env["sale.order"].sudo()

        for item in orders:
            woo_order_id = str(item.get("id"))
            if SaleOrder.search([("woo_order_id", "=", woo_order_id)], limit=1):
                skipped_count += 1
                continue

            partner = self._get_or_create_partner_from_order(item)
            order_lines = []
            booking = self._extract_booking_details(item)
            for line in item.get("line_items", []):
                product = self._get_or_create_product_from_order_line(line)
                if not booking:
                    booking = self._extract_booking_details(item, line)
                qty = float(line.get("quantity") or 1.0)
                subtotal = float(line.get("subtotal") or 0.0)
                price_unit = subtotal / qty if qty else float(line.get("price") or 0.0)
                order_lines.append((0, 0, {
                    "product_id": product.product_variant_id.id,
                    "name": line.get("name") or product.name,
                    "product_uom_qty": qty,
                    "price_unit": price_unit,
                }))

            if not order_lines:
                skipped_count += 1
                continue

            sale_order = False
            if config["create_sale_order"]:
                sale_order = SaleOrder.create({
                    "partner_id": partner.id,
                    "origin": "WooCommerce",
                    "client_order_ref": item.get("number") or woo_order_id,
                    "woo_order_id": woo_order_id,
                    "woo_order_key": item.get("order_key") or False,
                    "woo_status": item.get("status") or False,
                    "woo_sync_date": fields.Datetime.now(),
                    "woo_booking_service": booking.get("service") if booking else False,
                    "woo_booking_start": booking.get("start") if booking else False,
                    "woo_booking_stop": booking.get("stop") if booking else False,
                    "woo_booking_staff": booking.get("staff") if booking else False,
                    "woo_booking_notes": booking.get("notes") if booking else False,
                    "order_line": order_lines,
                })
                sale_count += 1

            event = False
            if config["create_calendar_event"] and booking and booking.get("start"):
                event = self._create_calendar_event_from_booking(
                    item,
                    partner,
                    booking,
                    sale_order=sale_order,
                    default_duration=config["default_booking_duration"],
                )
                appointment_count += 1

            if sale_order and event:
                sale_order.write({"woo_calendar_event_id": event.id})

        return self._show_notification(
            _("WooCommerce Import Complete"),
            _(
                "Created %(sales)s draft sales orders and %(appointments)s calendar appointments. Skipped %(skipped)s existing or empty orders."
            ) % {
                "sales": sale_count,
                "appointments": appointment_count,
                "skipped": skipped_count,
            },
        )

    def action_import_woo_bookings(self):
        return self.action_import_woo_orders()

    def action_import_salon_bookings(self):
        self.ensure_one()
        config = self._get_salon_config()
        response = self._salon_request("bookings", params={"per_page": min(config["limit"], 100)})
        bookings = response.get("bookings", []) if isinstance(response, dict) else []
        sale_count = 0
        appointment_count = 0
        skipped_count = 0
        SaleOrder = self.env["sale.order"].sudo()

        for booking in bookings:
            booking_id = str(booking.get("id") or "")
            if not booking_id:
                skipped_count += 1
                continue

            external_id = "SALON-%s" % booking_id
            if SaleOrder.search([("woo_order_id", "=", external_id)], limit=1):
                skipped_count += 1
                continue

            partner = self._get_or_create_partner_from_salon_booking(booking)
            product = self._get_or_create_product_from_salon_booking(booking)
            start = self._parse_booking_datetime(booking.get("start"), local_tz="Europe/London")
            stop = self._parse_booking_datetime(booking.get("stop"), local_tz="Europe/London")
            duration = float(booking.get("duration_hours") or 0.0)
            if start and not stop:
                stop = start + timedelta(hours=duration or config.get("default_booking_duration", 1.0) or 1.0)

            price = float(booking.get("price") or 0.0)
            service = self._clean_salon_service_name(booking.get("service")) or product.name
            notes = booking.get("notes") or False
            sale_order = SaleOrder.create({
                "partner_id": partner.id,
                "origin": "Salon Booking",
                "client_order_ref": booking_id,
                "woo_order_id": external_id,
                "woo_status": booking.get("status") or False,
                "woo_sync_date": fields.Datetime.now(),
                "woo_booking_service": service,
                "woo_booking_start": start,
                "woo_booking_stop": stop,
                "woo_booking_staff": booking.get("staff") or False,
                "woo_booking_notes": notes,
                "order_line": [(0, 0, {
                    "product_id": product.product_variant_id.id,
                    "name": service,
                    "product_uom_qty": 1.0,
                    "price_unit": price,
                })],
            })
            sale_count += 1

            if start:
                event = self._create_calendar_event_from_booking(
                    {"number": booking_id, "id": booking_id},
                    partner,
                    {
                        "service": service,
                        "start": start,
                        "stop": stop,
                        "staff": booking.get("staff"),
                        "notes": notes,
                    },
                    sale_order=sale_order,
                    default_duration=config.get("default_booking_duration", 1.0),
                )
                sale_order.write({"woo_calendar_event_id": event.id})
                appointment_count += 1

        return self._show_notification(
            _("Salon Import Complete"),
            _(
                "Created %(sales)s draft sales orders and %(appointments)s calendar appointments. Skipped %(skipped)s existing or invalid bookings."
            ) % {
                "sales": sale_count,
                "appointments": appointment_count,
                "skipped": skipped_count,
            },
        )

    # ---------------------------------------------------------------------
    # Calendar helpers
    # ---------------------------------------------------------------------

    def _create_calendar_event_from_booking(self, order, partner, booking, sale_order=False, default_duration=1.0):
        start = booking.get("start")
        stop = booking.get("stop") or start + timedelta(hours=default_duration or 1.0)
        service = self._clean_salon_service_name(booking.get("service")) or _("WooCommerce Booking")
        order_number = order.get("number") or order.get("id")
        description_lines = [
            _("WooCommerce Order: %s") % order_number,
            _("Service: %s") % service,
        ]
        if booking.get("staff"):
            description_lines.append(_("Staff: %s") % booking["staff"])
        if partner.email:
            description_lines.append(_("Email: %s") % partner.email)
        if partner.phone:
            description_lines.append(_("Phone: %s") % partner.phone)
        if sale_order:
            description_lines.append(_("Odoo Quotation: %s") % sale_order.name)
        if booking.get("notes"):
            description_lines.append("")
            description_lines.append(booking["notes"])

        partner_ids = [partner.id]
        user_partner = self.env.user.partner_id
        if user_partner and user_partner.id not in partner_ids:
            partner_ids.append(user_partner.id)

        return self.env["calendar.event"].sudo().create({
            "name": _("Woo Booking: %(service)s - %(customer)s") % {
                "service": service,
                "customer": partner.name,
            },
            "start": start,
            "stop": stop,
            "partner_ids": [(6, 0, partner_ids)],
            "description": "\n".join(description_lines),
        })

    # ---------------------------------------------------------------------
    # Booking metadata helpers
    # ---------------------------------------------------------------------

    def _extract_booking_details(self, order, line=None):
        service = line.get("name") if line else False
        source = line or order
        date_value = self._get_meta_value(source, [
            "booking_date", "appointment_date", "date", "start_date", "booked_date",
            "Booking Date", "Appointment Date", "Date",
        ])
        time_value = self._get_meta_value(source, [
            "booking_time", "appointment_time", "time", "start_time", "booked_time",
            "Booking Time", "Appointment Time", "Time",
        ])
        datetime_value = self._get_meta_value(source, [
            "booking_datetime", "appointment_datetime", "start", "starts_at",
            "Booking Start", "Appointment Start", "Start",
        ])
        stop_value = self._get_meta_value(source, [
            "booking_end", "appointment_end", "end", "ends_at", "end_time",
            "Booking End", "Appointment End", "End",
        ])
        staff = self._get_meta_value(source, [
            "staff", "employee", "resource", "provider", "Booking Staff", "Staff",
        ])
        metadata_service = self._get_meta_value(source, [
            "service", "booking_service", "appointment_service", "Service",
        ])
        notes = self._format_meta_notes(source)

        start = self._parse_booking_datetime(datetime_value, date_value, time_value)
        stop = self._parse_booking_datetime(stop_value, date_value, False) if stop_value else False
        service = metadata_service or service

        if not any([start, service, staff, notes]):
            return {}

        return {
            "service": service,
            "start": start,
            "stop": stop,
            "staff": staff,
            "notes": notes,
        }

    def _iter_woo_meta(self, item):
        for meta in item.get("meta_data", []) or []:
            key = meta.get("display_key") or meta.get("key")
            value = meta.get("display_value") or meta.get("value")
            if key and value not in (None, "", []):
                yield str(key), value

    def _get_meta_value(self, item, keys):
        wanted = {self._normalize_meta_key(key) for key in keys}
        for key, value in self._iter_woo_meta(item):
            if self._normalize_meta_key(key) in wanted:
                return self._plain_meta_value(value)
        return False

    def _normalize_meta_key(self, key):
        return re.sub(r"[^a-z0-9]+", "", str(key).lower())

    def _plain_meta_value(self, value):
        if isinstance(value, dict):
            return ", ".join("%s: %s" % (key, val) for key, val in value.items())
        if isinstance(value, list):
            return ", ".join(str(val) for val in value)
        return str(value).strip()

    def _parse_booking_datetime(self, datetime_value=False, date_value=False, time_value=False, local_tz=False):
        candidates = []
        if datetime_value:
            candidates.append(datetime_value)
            if "|" in datetime_value:
                left, right = datetime_value.split("|", 1)
                candidates.append("%s %s" % (left.strip(), right.strip()))
        if date_value and time_value:
            candidates.append("%s %s" % (date_value, time_value))
        if date_value and not time_value:
            candidates.append(date_value)

        for candidate in candidates:
            try:
                parsed = parser.parse(candidate, fuzzy=True)
                if parsed.tzinfo:
                    parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
                elif local_tz:
                    parsed = parsed.replace(tzinfo=ZoneInfo(local_tz)).astimezone(timezone.utc).replace(tzinfo=None)
                return parsed
            except (TypeError, ValueError, OverflowError):
                continue
        return False

    def _format_meta_notes(self, item):
        notes = []
        for key, value in self._iter_woo_meta(item):
            if key.startswith("_"):
                continue
            notes.append("%s: %s" % (key, self._plain_meta_value(value)))
        return "\n".join(notes) if notes else False

    # ---------------------------------------------------------------------
    # Mapping helpers
    # ---------------------------------------------------------------------

    def _get_or_create_partner_from_order(self, order):
        Partner = self.env["res.partner"].sudo()
        billing = order.get("billing") or {}
        customer_id = order.get("customer_id")
        woo_id = str(customer_id) if customer_id else False
        email = billing.get("email") or ""

        partner = False
        if woo_id and woo_id != "0":
            partner = Partner.search([("woo_id", "=", woo_id)], limit=1)
        if not partner and email:
            partner = Partner.search([("email", "=", email)], limit=1)

        first_name = billing.get("first_name") or ""
        last_name = billing.get("last_name") or ""
        name = (first_name + " " + last_name).strip() or billing.get("company") or email or _("WooCommerce Guest")
        vals = {
            "name": name,
            "woo_id": woo_id if woo_id and woo_id != "0" else False,
            "email": email or False,
            "phone": billing.get("phone") or False,
            "street": billing.get("address_1") or False,
            "street2": billing.get("address_2") or False,
            "city": billing.get("city") or False,
            "zip": billing.get("postcode") or False,
            "woo_sync_date": fields.Datetime.now(),
        }
        if partner:
            partner.write(vals)
            return partner
        return Partner.create(vals)

    def _get_or_create_partner_from_salon_booking(self, booking):
        Partner = self.env["res.partner"].sudo()
        customer = booking.get("customer") or {}
        email = customer.get("email") or booking.get("email") or ""
        phone = customer.get("phone") or booking.get("phone") or ""
        name = (
            customer.get("name")
            or booking.get("customer_name")
            or " ".join(filter(None, [customer.get("first_name"), customer.get("last_name")]))
            or email
            or _("Salon Customer")
        )

        partner = Partner.search([("email", "=", email)], limit=1) if email else False
        vals = {
            "name": name,
            "email": email or False,
            "phone": phone or False,
            "woo_sync_date": fields.Datetime.now(),
        }
        if partner:
            partner.write(vals)
            return partner
        return Partner.create(vals)

    def _get_or_create_product_from_order_line(self, line):
        Product = self.env["product.template"].sudo()
        woo_product_id = str(line.get("product_id")) if line.get("product_id") else False
        sku = line.get("sku") or ""
        product = False

        if woo_product_id:
            product = Product.search([("woo_id", "=", woo_product_id)], limit=1)
        if not product and sku:
            product = Product.search([("default_code", "=", sku)], limit=1)

        if product:
            return product

        return Product.create({
            "name": line.get("name") or _("WooCommerce Product"),
            "woo_id": woo_product_id,
            "woo_sku": sku,
            "default_code": sku or False,
            "list_price": float(line.get("price") or 0.0),
            "sale_ok": True,
            "purchase_ok": False,
            "woo_sync_date": fields.Datetime.now(),
        })

    def _get_or_create_product_from_salon_booking(self, booking):
        Product = self.env["product.template"].sudo()
        service = self._clean_salon_service_name(booking.get("service")) or _("Salon Booking Service")
        default_code = "SALON-%s" % self._normalize_meta_key(service).upper()[:30]
        product = Product.search([("default_code", "=", default_code)], limit=1)
        if product:
            return product
        return Product.create({
            "name": service,
            "default_code": default_code,
            "list_price": float(booking.get("price") or 0.0),
            "sale_ok": True,
            "purchase_ok": False,
            "woo_sync_date": fields.Datetime.now(),
        })

    def _clean_salon_service_name(self, service):
        if not service:
            return False
        service = str(service).strip()
        for service_id, service_name in self.SALON_SERVICE_NAMES.items():
            if ('"service";i:%s' % service_id) in service or ("'service';i:%s" % service_id) in service:
                return service_name
        if service.startswith("a:") and "service" in service:
            return _("Salon Booking Service")
        return service
