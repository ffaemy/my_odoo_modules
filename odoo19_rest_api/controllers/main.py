import json

from odoo import http
from odoo.http import request


class Odoo19RestApiController(http.Controller):
    """Simple REST API demo controller for Odoo 19.

    Header required:
        Authorization: Bearer YOUR_API_KEY
    """

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _json_response(self, data, status=200):
        return request.make_response(
            json.dumps(data, default=str),
            headers=[("Content-Type", "application/json")],
            status=status,
        )

    def _get_request_data(self):
        """Read JSON body safely."""
        try:
            raw_data = request.httprequest.get_data(as_text=True)
            if not raw_data:
                return {}
            return json.loads(raw_data)
        except Exception:
            return None

    def _check_api_key(self):
        """Validate API key from Authorization header."""
        configured_key = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("odoo19_rest_api.api_key")
        )

        if not configured_key:
            return False, {
                "success": False,
                "error": "API key is not configured in Odoo settings.",
            }

        auth_header = request.httprequest.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return False, {
                "success": False,
                "error": "Missing or invalid Authorization header. Use: Bearer YOUR_API_KEY",
            }

        provided_key = auth_header.removeprefix("Bearer ").strip()

        if provided_key != configured_key:
            return False, {
                "success": False,
                "error": "Invalid API key.",
            }

        return True, {}

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    @http.route(
        "/api/health",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def api_health(self, **kwargs):
        return self._json_response({
            "success": True,
            "message": "Odoo 19 REST API is running.",
        })

    # -------------------------------------------------------------------------
    # GET Products
    # -------------------------------------------------------------------------

    @http.route(
        "/api/products",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_products(self, **kwargs):
        valid, error = self._check_api_key()
        if not valid:
            return self._json_response(error, status=401)

        try:
            limit = int(kwargs.get("limit", 20))
        except (TypeError, ValueError):
            return self._json_response({
                "success": False,
                "error": "limit must be an integer.",
            }, status=400)

        products = request.env["product.product"].sudo().search(
            [("sale_ok", "=", True)],
            limit=limit,
        )

        product_data = []
        for product in products:
            product_data.append({
                "id": product.id,
                "name": product.display_name,
                "default_code": product.default_code or "",
                "list_price": product.lst_price,
                "uom": product.uom_id.name if product.uom_id else "",
                "available_qty": product.qty_available,
            })

        return self._json_response({
            "success": True,
            "count": len(product_data),
            "products": product_data,
        })

    # -------------------------------------------------------------------------
    # POST Create Customer
    # -------------------------------------------------------------------------

    @http.route(
        "/api/customer/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_customer(self, **kwargs):
        valid, error = self._check_api_key()
        if not valid:
            return self._json_response(error, status=401)

        data = self._get_request_data()
        if data is None:
            return self._json_response({
                "success": False,
                "error": "Invalid JSON body.",
            }, status=400)

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        company_name = data.get("company_name")

        if not name:
            return self._json_response({
                "success": False,
                "error": "Customer name is required.",
            }, status=400)

        partner_vals = {
            "name": name,
            "email": email,
            "phone": phone,
            "company_name": company_name,
            "customer_rank": 1,
        }

        partner = request.env["res.partner"].sudo().create(partner_vals)

        return self._json_response({
            "success": True,
            "message": "Customer created successfully.",
            "customer": {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email or "",
                "phone": partner.phone or "",
            },
        }, status=201)

    # -------------------------------------------------------------------------
    # POST Create Sale Order
    # -------------------------------------------------------------------------

    @http.route(
        "/api/sale_order/create",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def create_sale_order(self, **kwargs):
        valid, error = self._check_api_key()
        if not valid:
            return self._json_response(error, status=401)

        data = self._get_request_data()
        if data is None:
            return self._json_response({
                "success": False,
                "error": "Invalid JSON body.",
            }, status=400)

        partner_id = data.get("partner_id")
        order_lines = data.get("order_lines", [])

        if not partner_id:
            return self._json_response({
                "success": False,
                "error": "partner_id is required.",
            }, status=400)

        try:
            partner_id = int(partner_id)
        except (TypeError, ValueError):
            return self._json_response({
                "success": False,
                "error": "partner_id must be an integer.",
            }, status=400)

        partner = request.env["res.partner"].sudo().browse(partner_id)
        if not partner.exists():
            return self._json_response({
                "success": False,
                "error": "Customer not found.",
            }, status=404)

        if not order_lines:
            return self._json_response({
                "success": False,
                "error": "order_lines are required.",
            }, status=400)

        sale_order_lines = []

        for line in order_lines:
            product_id = line.get("product_id")
            quantity = line.get("quantity", 1)

            if not product_id:
                return self._json_response({
                    "success": False,
                    "error": "product_id is required for each order line.",
                }, status=400)

            try:
                product_id = int(product_id)
                quantity = float(quantity)
            except (TypeError, ValueError):
                return self._json_response({
                    "success": False,
                    "error": "product_id must be an integer and quantity must be numeric.",
                }, status=400)

            product = request.env["product.product"].sudo().browse(product_id)
            if not product.exists():
                return self._json_response({
                    "success": False,
                    "error": f"Product not found: {product_id}",
                }, status=404)

            sale_order_lines.append((0, 0, {
                "product_id": product.id,
                "product_uom_qty": quantity,
                "price_unit": line.get("price_unit", product.lst_price),
            }))

        sale_order = request.env["sale.order"].sudo().create({
            "partner_id": partner.id,
            "order_line": sale_order_lines,
            "origin": data.get("origin", "External REST API"),
            "client_order_ref": data.get("client_order_ref"),
        })

        return self._json_response({
            "success": True,
            "message": "Sale Order created successfully.",
            "sale_order": {
                "id": sale_order.id,
                "name": sale_order.name,
                "partner_id": sale_order.partner_id.id,
                "partner_name": sale_order.partner_id.name,
                "amount_total": sale_order.amount_total,
                "state": sale_order.state,
            },
        }, status=201)
