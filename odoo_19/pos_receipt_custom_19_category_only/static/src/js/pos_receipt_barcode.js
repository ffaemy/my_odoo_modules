/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

const DEFAULT_BARCODE_TYPE = "Code128";

patch(PosOrder.prototype, {
    /**
     * Value rendered as barcode on the receipt.
     * Falls back to the POS uid while the order has no final name yet.
     */
    get receiptBarcodeValue() {
        if (this.name && this.name !== "/") {
            return this.name;
        }
        return this.uid;
    },

    /**
     * URL to the server-side barcode generator route.
     */
    get receiptBarcodeUrl() {
        const value = this.receiptBarcodeValue;
        if (!value) {
            return "";
        }
        const type = this.config?.receipt_barcode_type || DEFAULT_BARCODE_TYPE;
        const baseUrl =
            (this.config?._base_url || window.location.origin || "").replace(/\/+$/, "");
        const prefix = baseUrl || "";
        return `${prefix}/report/barcode/${encodeURIComponent(type)}/${encodeURIComponent(
            value
        )}?width=400&height=100&humanreadable=1`;
    },
});
