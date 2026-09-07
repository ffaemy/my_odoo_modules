/** @odoo-module */

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    /**
     * Expose the first POS category name so it can be templated easily.
     */
    get categoryName() {
        const categories = this.product_id?.pos_categ_ids || [];
        return categories.length ? categories[0].name : "";
    },
});
