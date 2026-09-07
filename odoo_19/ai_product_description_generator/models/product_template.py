import requests

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ai_generated_description = fields.Html(
        string="AI Generated Description",
        readonly=True,
        copy=False,
    )

    def action_generate_ai_description(self):
        api_key = self.env["ir.config_parameter"].sudo().get_param(
            "ai_product_description.gemini_api_key"
        )

        model = self.env["ir.config_parameter"].sudo().get_param(
            "ai_product_description.gemini_model",
            default="gemini-2.5-flash",
        )

        if not api_key:
            raise UserError(_("Please configure your Gemini API Key in Settings."))

        for product in self:
            prompt = product._prepare_ai_product_prompt()

            ai_text = product._call_gemini_api(
                api_key=api_key,
                model=model,
                prompt=prompt,
            )

            # Save raw AI output
            product.ai_generated_description = ai_text

            # description_sale is a plain text field in Odoo's default product form.
            product.description_sale = ai_text

        return True

    def _prepare_ai_product_prompt(self):
        self.ensure_one()

        category = self.categ_id.name if self.categ_id else "General"
        price = self.list_price or 0.0

        return f"""
You are an expert eCommerce copywriter.

Write a HIGH-QUALITY product description.

Product:
- Name: {self.name}
- Category: {category}
- Price: {price}

Output format:

Short Description:
(1–2 lines)

Detailed Description:
(engaging paragraph)

Key Features:
- bullet points

SEO Meta Description:
(max 160 characters)

Tone: Professional and persuasive
"""

    def _call_gemini_api(self, api_key, model, prompt):
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent"
        )

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
            },
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                params={"key": api_key},
                timeout=30,
            )
            result = response.json()
            if response.status_code >= 400:
                message = result.get("error", {}).get("message") or response.text
                raise UserError(_("Gemini API Error: %s") % message)

            parts = result["candidates"][0]["content"]["parts"]
            text = "\n".join(part.get("text", "") for part in parts).strip()
            if not text:
                raise UserError(_("Gemini returned an empty response."))
            return text

        except UserError:
            raise
        except Exception as e:
            raise UserError(_("AI Error: %s") % str(e))
