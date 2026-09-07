/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PriceOverrideDialog } from "./price_override_dialog";

function priceOverrideAction(env, action) {
    const orderId = action?.params?.order_id || action?.context?.order_id || action?.res_id;

    if (!orderId) {
        env.services.notification?.add("Unable to open Price Override: missing Sale Order ID.", {
            type: "danger",
        });
        return;
    }

    env.services.dialog.add(PriceOverrideDialog, { orderId: Number(orderId) });
}

registry.category("actions").add("odooistic_price_override_wizard.action", priceOverrideAction, {
    force: true,
});
