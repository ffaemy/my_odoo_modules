/** @odoo-module **/
import { registry } from "@web/core/registry";
registry.category("services").add("okc_boot", {
    start() {
        console.log("[OKC] assets loaded");
        window.OKC_ASSETS_LOADED = true;
    },
});
