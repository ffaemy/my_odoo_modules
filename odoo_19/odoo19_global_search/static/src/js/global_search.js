/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

const systrayRegistry = registry.category("systray");

export class GlobalSearch extends Component {
    setup() {
        this.action = useService("action");
        this.state = useState({
            open: false,
            query: "",
            loading: false,
            results: [],
        });
        this.inputRef = useRef("input");
    }

    // ---------- Open / close panel ----------
    openPanel() {
        this.state.open = true;
        this.state.query = "";
        this.state.results = [];
        this.state.loading = false;
        setTimeout(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
        }, 50);
    }

    closePanel() {
        this.state.open = false;
    }

    togglePanel() {
        if (this.state.open) {
            this.closePanel();
        } else {
            this.openPanel();
        }
    }

    // ---------- Input -> search ----------
    onInput(ev) {
        this.state.query = ev.target.value;
        this.search();
    }

    async search() {
        const query = this.state.query.trim();
        if (!query) {
            this.state.results = [];
            return;
        }
        this.state.loading = true;
        try {
            const res = await rpc("/odoo19_global_search/search", { query });
            this.state.results = res.results || [];
        } catch (e) {
            console.error("Global search RPC error", e);
            this.state.results = [];
        } finally {
            this.state.loading = false;
        }
    }

    // ---------- Click on a result row ----------
    async onResultClick(ev) {
        const el = ev.currentTarget;
        if (!el) {
            return;
        }
        const model = el.dataset.model;
        const idStr = el.dataset.id;
        if (!model || !idStr) {
            return;
        }
        const resId = parseInt(idStr, 10);
        if (!resId) {
            return;
        }

        this.closePanel();

        await this.action.doAction({
            type: "ir.actions.act_window",
            res_model: model,
            res_id: resId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

GlobalSearch.template = "odoo19_global_search.GlobalSearch";

systrayRegistry.add("odoo19_global_search.GlobalSearch", {
    Component: GlobalSearch,
    props: {},
    sequence: 10,
});
