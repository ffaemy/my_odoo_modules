/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class PriceOverrideDialog extends Component {
    static template = "odooistic_price_override_wizard.PriceOverrideDialog";
    static props = {
        orderId: Number,
        close: { type: Function, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            discount: 10,
            loading: false,
            preview: null,
            error: null,
        });

        onWillStart(async () => {
            await this.fetchPreview();
        });
    }

    async fetchPreview() {
        this.state.loading = true;
        this.state.error = null;
        try {
            const res = await this.orm.call(
                "sale.order",
                "price_override_preview",
                [this.props.orderId, this.state.discount],
                {}
            );
            if (res?.error) {
                this.state.error = res.error;
                this.state.preview = null;
            } else {
                this.state.preview = res;
            }
        } catch (e) {
            this.state.error = "Failed to load preview.";
            this.state.preview = null;
        } finally {
            this.state.loading = false;
        }
    }

    formatMoney(amount) {
        const p = this.state.preview;
        const value = Number(amount || 0).toFixed(2);
        if (!p) return value;

        const sym = p.currency_symbol || "";
        const pos = p.currency_position || "before";
        return pos === "after" ? `${value} ${sym}` : `${sym} ${value}`;
    }

    async onDiscountInput(ev) {
        const v = Number(ev.target.value || 0);
        this.state.discount = Math.max(0, Math.min(100, v));
        await this.fetchPreview();
    }

    close() {
        if (this.props.close) {
            this.props.close();
        }
    }

    async apply() {
        this.state.loading = true;
        this.state.error = null;
        try {
            const res = await this.orm.call(
                "sale.order",
                "price_override_apply_bulk_discount",
                [this.props.orderId, this.state.discount],
                {}
            );
            if (res?.error) {
                this.state.error = res.error;
                return;
            }
            this.close();
            await this.action.doAction({ type: "ir.actions.client", tag: "reload" });
        } catch (e) {
            this.state.error = "Failed to apply discount.";
        } finally {
            this.state.loading = false;
        }
    }
}
