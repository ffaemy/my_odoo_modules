from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ai_gemini_api_key = fields.Char(
        string="Gemini API Key",
        config_parameter="ai_product_description.gemini_api_key",
    )

    ai_gemini_model = fields.Char(
        string="Gemini Model",
        default="gemini-2.5-flash",
        config_parameter="ai_product_description.gemini_model",
    )
