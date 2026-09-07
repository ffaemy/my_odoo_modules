from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    odoo19_rest_api_key = fields.Char(
        string="REST API Key",
        config_parameter="odoo19_rest_api.api_key",
        help="API key required in the Authorization header. Example: Bearer YOUR_API_KEY",
    )
