#!/usr/bin/env bash
# Quick smoke test for the odoo19_rest_api module.
# Usage:
#   BASE_URL=http://localhost:8077 API_KEY=your_key ./smoke.sh
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8077}"
API_KEY="${API_KEY:?Set API_KEY to the value configured in Settings.}"
AUTH="Authorization: Bearer ${API_KEY}"
JSON="Content-Type: application/json"

section() { printf "\n\033[1;34m==> %s\033[0m\n" "$*"; }

section "Health check (no auth)"
curl -sS "${BASE_URL}/api/health" | python3 -m json.tool

section "Get products (limit=3)"
curl -sS -H "${AUTH}" "${BASE_URL}/api/products?limit=3" | python3 -m json.tool

section "Create customer"
PARTNER_JSON=$(curl -sS -X POST "${BASE_URL}/api/customer/create" \
    -H "${AUTH}" -H "${JSON}" \
    -d '{"name":"ACME Ltd","email":"hello@acme.test","phone":"+441234567890","company_name":"ACME Ltd"}')
echo "${PARTNER_JSON}" | python3 -m json.tool
PARTNER_ID=$(echo "${PARTNER_JSON}" | python3 -c "import sys,json;print(json.load(sys.stdin)['customer']['id'])")

section "Create sale order for partner ${PARTNER_ID}"
PRODUCT_ID=$(curl -sS -H "${AUTH}" "${BASE_URL}/api/products?limit=1" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['products'][0]['id'])")
curl -sS -X POST "${BASE_URL}/api/sale_order/create" \
    -H "${AUTH}" -H "${JSON}" \
    -d "{\"partner_id\":${PARTNER_ID},\"origin\":\"smoke.sh\",\"order_lines\":[{\"product_id\":${PRODUCT_ID},\"quantity\":2}]}" \
    | python3 -m json.tool

section "Negative — bad key returns 401"
curl -sS -o /dev/null -w "HTTP %{http_code}\n" \
    -H "Authorization: Bearer not-the-real-key" "${BASE_URL}/api/products"
