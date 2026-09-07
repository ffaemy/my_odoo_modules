# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class GlobalSearchController(http.Controller):

    @http.route("/odoo19_global_search/search", type="json", auth="user")
    def global_search(self, query="", **kwargs):
        """Return a flat list of search results across key models."""
        query = (query or "").strip()
        if not query:
            return {"results": []}

        env = request.env
        max_per_model = 5
        results = []

        def add_results(model, label, domain, subtitle_getter=None):
            try:
                records = env[model].search(domain, limit=max_per_model)
            except Exception:
                # If model or field does not exist or access denied, skip silently.
                return
            for rec in records:
                subtitle = ""
                if subtitle_getter:
                    try:
                        subtitle_val = subtitle_getter(rec)
                        subtitle = subtitle_val or ""
                    except Exception:
                        subtitle = ""
                display_name = rec.display_name or getattr(rec, "name", str(rec.id))
                results.append(
                    {
                        "key": f"{model}-{rec.id}",
                        "model": model,
                        "model_label": label,
                        "id": rec.id,
                        "display_name": display_name,
                        "subtitle": subtitle,
                    }
                )

        q = query

        # Sale Orders
        add_results(
            "sale.order",
            "Sale Order",
            ["|", ("name", "ilike", q), ("partner_id.name", "ilike", q)],
            subtitle_getter=lambda r: r.partner_id.display_name,
        )

        # Invoices / Bills
        add_results(
            "account.move",
            "Invoice / Bill",
            [
                "|",
                "|",
                ("name", "ilike", q),
                ("ref", "ilike", q),
                ("partner_id.name", "ilike", q),
            ],
            subtitle_getter=lambda r: r.partner_id.display_name,
        )

        # Contacts
        add_results(
            "res.partner",
            "Contact",
            [
                "|",
                "|",
                ("name", "ilike", q),
                ("email", "ilike", q),
                ("phone", "ilike", q),
            ],
            subtitle_getter=lambda r: r.email or r.phone or "",
        )

        # Products
        add_results(
            "product.template",
            "Product",
            [
                "|",
                ("name", "ilike", q),
                ("default_code", "ilike", q),
            ],
            subtitle_getter=lambda r: r.default_code,
        )

        return {"results": results}
