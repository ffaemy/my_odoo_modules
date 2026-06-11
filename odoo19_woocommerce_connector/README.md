# Odoo 19 WooCommerce Connector

Tutorial/demo connector for Odoo 19 and WooCommerce.

## Features

- WooCommerce settings section in Odoo Settings
- Store URL, Consumer Key, Consumer Secret
- Test Connection button
- Import Products
- Import Customers
- Import Orders into Odoo Sales Orders
- Import booking orders into draft quotations
- Create Odoo Calendar appointments from WooCommerce booking date/time metadata
- Import bookings directly from Salon Booking System using the included WordPress helper plugin

## WooCommerce API Setup

In WordPress:

1. Go to **WooCommerce → Settings → Advanced → REST API**
2. Click **Add Key**
3. Description: `Odoo 19 Integration`
4. User: select your admin user
5. Permissions: `Read/Write`
6. Click **Generate API Key**
7. Copy Consumer Key and Consumer Secret

## Odoo Setup

1. Copy this module into your custom addons path.
2. Restart Odoo.
3. Update Apps List.
4. Install **Odoo 19 WooCommerce Connector**.
5. Go to **Settings → WooCommerce**.
6. Enter Store URL, Consumer Key and Consumer Secret.
7. Click **Test Connection**.
8. Enable **Create Draft Sale Order** and **Create Calendar Appointment** for the booking demo.

## Demo Flow for YouTube

1. Show WooCommerce API keys.
2. Install this Odoo module.
3. Open Settings → WooCommerce.
4. Add credentials.
5. Test connection.
6. Import Products.
7. Import Customers.
8. Import Bookings.
9. Show the customer contact, draft quotation and linked calendar appointment in Odoo.

## Direct Salon Booking Import

WooCommerce orders only work when the booking plugin creates WooCommerce orders. If bookings are stored under **WordPress → Salon → Bookings**, install the helper plugin from:

`wordpress_plugins/odoo_salon_api/odoo_salon_api.php`

In WordPress:

1. Install/activate **Odoo Salon Booking API**.
2. Go to **Settings → Odoo Salon API**.
3. Copy the API token.

In Odoo:

1. Go to **Settings → WooCommerce**.
2. Set **Salon API URL** to your website URL, for example `https://ifairbeautyandhair.com`.
3. Paste the token into **Salon API Token**.
4. Click **Test Salon API**.
5. Click **Import Salon Bookings**.

## Booking Demo Flow

When a booking order is imported:

1. Odoo finds or creates the customer contact by WooCommerce customer ID or email.
2. Odoo creates a draft quotation with the booked service as the order line.
3. Odoo reads common booking metadata keys such as `Booking Date`, `Appointment Time`, `Start`, `Staff` and `Service`.
4. If a booking start date/time is found, Odoo creates a Calendar appointment and links it back to the quotation.

## Notes

This module is intentionally simple for tutorial usage. For production, add pagination, queues, cron jobs, webhooks, taxes, shipping mapping, payment mapping, multi-company support, stock push-back, booking plugin specific field mapping, timezone rules and error logs.
