# Odoo 19 REST API Demo

This module adds simple REST API endpoints to Odoo 19.

## Endpoints

### Health Check

GET `/api/health`

### Get Products

GET `/api/products?limit=10`

Header:

```text
Authorization: Bearer YOUR_API_KEY
```

### Create Customer

POST `/api/customer/create`

Header:

```text
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Body:

```json
{
    "name": "Test Customer",
    "email": "test@example.com",
    "phone": "+441234567890",
    "company_name": "Test Company"
}
```

### Create Sale Order

POST `/api/sale_order/create`

Header:

```text
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Body:

```json
{
    "partner_id": 1,
    "origin": "Website",
    "client_order_ref": "WEB-1001",
    "order_lines": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}
```

## Setup

1. Copy this module into your custom addons folder.
2. Update Apps List.
3. Install **Odoo 19 REST API Demo**.
4. Go to Settings.
5. Open **Odoo 19 REST API** section.
6. Set your API key.
7. Test with Postman.

## Custom REST vs Odoo 19's new `/json/2` API

Odoo 19 ships a new built-in external API at `/json/2/{model}/{method}` that replaces the legacy XML-RPC and JSON-RPC endpoints. Before building a custom REST controller, it's worth knowing what you get for free.

**Built-in `/json/2` (no custom code needed):**

```bash
curl -X POST http://localhost:8077/json/2/res.partner/create \
     -H "Authorization: Bearer USER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"args": [[{"name": "ACME Ltd", "email": "hello@acme.test"}]]}'
```

- Auth: per-user API keys (created from the user's preferences).
- Permissions: full Odoo ACL / record-rules — you call as a real user.
- Surface: any model, any public method. Same payload shape as ORM calls.
- Trade-off: clients have to know Odoo's model names, field names, and ORM idioms (`args`, `kwargs`, tuple commands like `(0, 0, {...})`).

**This module's custom REST controller:**

```bash
curl -X POST http://localhost:8077/api/customer/create \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"name": "ACME Ltd", "email": "hello@acme.test"}'
```

- Auth: shared API key stored in Settings (one secret for the whole integration).
- Permissions: runs as `sudo()` — the controller decides what's allowed.
- Surface: only the endpoints you publish; clients see a stable, REST-shaped contract.
- Trade-off: every new operation is code you write and maintain.

**Pick the custom controller when:**
- External callers shouldn't need to know Odoo's data model.
- You want stable URLs and a fixed JSON shape that survives Odoo upgrades.
- You're exposing a small, curated set of operations to an integration partner.

**Use `/json/2` directly when:**
- The caller is internal/trusted and you want every model exposed.
- You're prototyping or scripting from outside Odoo and want zero server-side code.
- You need per-user audit trails and ACLs without writing them.

A common production pattern is both: `/json/2` for in-house tooling, a custom REST module for partner-facing integrations.

## Testing

### Bash smoke test (curl)

```bash
cd tests
BASE_URL=http://localhost:8077 API_KEY=your_key ./smoke.sh
```

Hits every endpoint top-to-bottom and verifies the negative case (bad API key → 401).

### Postman collection

Import `tests/postman_collection.json` into Postman, then in the collection variables set:

- `base_url` — e.g. `http://localhost:8077`
- `api_key` — the value from **Settings → Odoo 19 REST API**

Run the collection from top to bottom. The "Get Products" and "Create Customer" requests capture IDs into collection variables, so "Create Sale Order" works without manual edits.
