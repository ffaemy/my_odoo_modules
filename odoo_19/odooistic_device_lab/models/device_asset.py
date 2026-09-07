import logging

from odoo import _, api, fields, models


_logger = logging.getLogger(__name__)


class DeviceAsset(models.Model):
    _name = "device.asset"
    _description = "Device Asset"
    _order = "id desc"

    name = fields.Char(
        string="Device Name",
        required=True,
        index=True,
    )

    serial_number = fields.Char(
        string="Serial Number",
        required=True,
        index=True,
    )

    device_type = fields.Selection(
        selection=[
            ("laptop", "Laptop"),
            ("desktop", "Desktop"),
            ("mobile", "Mobile Phone"),
            ("tablet", "Tablet"),
        ],
        string="Device Type",
        default="laptop",
        required=True,
    )

    status = fields.Selection(
        selection=[
            ("received", "Received"),
            ("wiping", "Wiping"),
            ("graded", "Graded"),
            ("ready", "Ready for Sale"),
            ("sold", "Sold"),
        ],
        string="Status",
        default="received",
        required=True,
        index=True,
    )

    grade = fields.Selection(
        selection=[
            ("a", "Grade A"),
            ("b", "Grade B"),
            ("c", "Grade C"),
        ],
        string="Grade",
    )

    cost_price = fields.Monetary(
        string="Cost Price",
    )

    selling_price = fields.Monetary(
        string="Selling Price",
    )

    margin = fields.Monetary(
        string="Margin",
        compute="_compute_margin",
        store=True,
    )

    active = fields.Boolean(
        default=True,
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )

    @api.depends(
        "cost_price",
        "selling_price",
    )
    def _compute_margin(self):
        for device in self:
            device.margin = (
                device.selling_price
                - device.cost_price
            )

    def action_cache_prefetch_demo(self):
        """
        Read several stored fields from one recordset.

        Start Odoo with --log-sql and use this method
        to observe prefetching and ORM cache behaviour.
        """

        devices = self.search([
            ("active", "=", True),
        ], limit=100)

        values = [
            (
                device.name,
                device.serial_number,
                device.grade,
                device.selling_price,
            )
            for device in devices
        ]

        _logger.info(
            "ODOOISTIC PREFETCH DEMO: "
            "read %s devices from one recordset: %s",
            len(devices),
            values,
        )

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _(
                    "Cache and Prefetch Demo"
                ),
                "message": _(
                    "%s device records were read. "
                    "Check the Odoo SQL log to inspect "
                    "the generated database queries."
                ) % len(devices),
                "type": "success",
                "sticky": False,
            },
        }

    def action_increase_ready_prices(self):
        """
        Increase prices using raw SQL while correctly
        synchronising the ORM cache.
        """

        Device = self.env["device.asset"]

        # Flush fields used by the SQL statement.
        Device.flush_model([
            "selling_price",
            "status",
        ])

        # Parameterised raw SQL update.
        # RETURNING provides the affected record IDs.
        self.env.cr.execute(
            """
                UPDATE device_asset
                   SET selling_price = selling_price * 1.05
                 WHERE status = %s
             RETURNING id
            """,
            ("ready",),
        )

        device_ids = [
            row[0]
            for row in self.env.cr.fetchall()
        ]

        devices = Device.browse(device_ids)

        # Remove stale selling prices from the cache.
        devices.invalidate_recordset([
            "selling_price",
        ])

        # Notify the ORM dependency system.
        # This allows stored margin values to be updated.
        devices.modified([
            "selling_price",
        ])

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _(
                    "Raw SQL Update Complete"
                ),
                "message": _(
                    "%s ready-device prices were "
                    "increased by 5 percent."
                ) % len(devices),
                "type": "success",
                "sticky": False,
                "next": {
                    "type": "ir.actions.client",
                    "tag": "reload",
                },
            },
        }