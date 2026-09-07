/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const WARNING_DAYS = 2;

// ---- Color helpers ----
function colorFromMetrics(m) {
    if (!m) return { cls: "", hex: "" };
    if (m.is_done) return { cls: "okc-card--green", hex: "#22c55e" };
    if (typeof m.deadline_days_left === "number") {
        if (m.deadline_days_left < 0) return { cls: "okc-card--red", hex: "#ef4444" };
        if (m.deadline_days_left <= WARNING_DAYS) return { cls: "okc-card--orange", hex: "#f59e0b" };
    }
    if ((m.unread_count || 0) > 0) return { cls: "okc-card--blue", hex: "#3b82f6" };
    return { cls: "", hex: "" };
}

function colorFromColumn(el) {
    const col = el.closest(".o_kanban_group");
    const title = (col?.querySelector(".o_kanban_header, .o_kanban_group_header")?.textContent || "")
        .toLowerCase();

    // Adjust these to your exact stage names if needed
    if (title.includes("won") || title.includes("done") || title.includes("closed")) return { cls: "okc-card--green",  hex: "#22c55e" };
    if (title.includes("proposition")) return { cls: "okc-card--orange", hex: "#f59e0b" };
    if (title.includes("qualified"))   return { cls: "okc-card--blue",   hex: "#3b82f6" };
    if (title.includes("new"))         return { cls: "okc-card--red",    hex: "#ef4444" };
    return { cls: "okc-card--blue", hex: "#3b82f6" };
}

function buildTooltip(m) {
    if (!m) return "";
    const parts = [];
    parts.push(typeof m.deadline_days_left === "number" ? `Deadline in ${m.deadline_days_left} day(s)` : "No deadline");
    parts.push(`Activities: ${m.activities_count ?? 0}`);
    parts.push(`Unread: ${m.unread_count ?? 0}`);
    if (typeof m.subtask_count === "number") parts.push(`Subtasks: ${m.subtask_count}`);
    if (m.is_done) parts.push("Status: Completed");
    return parts.join(" • ");
}

// ---- Record id extraction (handles hash-style URLs) ----
function getResId(el) {
    // 1) data-* attributes on the card
    const raw = el.dataset?.id || el.dataset?.resId || el.getAttribute("data-id") || el.getAttribute("data-res-id");
    const n1 = Number(raw);
    if (Number.isFinite(n1)) return n1;

    // 2) Anchors inside the card
    const a = el.querySelector('a[href*="id="], a[href*="/id/"], a[href^="#"], a[href*="#"]');
    if (a) {
        const href = a.getAttribute("href") || "";

        // 2a) Odoo hash URLs: /web#id=123&model=crm.lead...
        const hash = href.includes("#") ? href.split("#")[1] : "";
        if (hash) {
            const params = Object.fromEntries(hash.split("&").map(kv => kv.split("=").map(decodeURIComponent)));
            const hid = Number(params.id);
            if (Number.isFinite(hid)) return hid;
        }

        // 2b) Query-style
        try {
            const url = new URL(href, location.origin);
            const qid = Number(url.searchParams.get("id"));
            if (Number.isFinite(qid)) return qid;
        } catch {/* ignore */}

        // 2c) /id/123
        const m = href.match(/\/id\/(\d+)/);
        if (m) return Number(m[1]);
    }

    // 3) Inner clickable carrying data-id
    const click = el.querySelector('.oe_kanban_global_click, .o_kanban_record_title, a[data-id]');
    if (click) {
        const raw2 = click.getAttribute("data-id");
        const n2 = Number(raw2);
        if (Number.isFinite(n2)) return n2;
    }
    return null;
}

// ---- Visual helpers ----
function ensureStripe(el, hex = "#3b82f6") {
    let stripe = el.querySelector(":scope > .okc-stripe");
    if (!stripe) {
        stripe = document.createElement("div");
        stripe.className = "okc-stripe";
        stripe.style.position = "absolute";
        stripe.style.left = "0";
        stripe.style.top = "0";
        stripe.style.bottom = "0";
        stripe.style.width = "6px";
        stripe.style.zIndex = "2";
        stripe.style.pointerEvents = "none";
        if (!el.style.position) el.style.position = "relative";
        if (!el.style.overflow) el.style.overflow = "visible";
        el.prepend(stripe);
    }
    stripe.style.background = hex;
    el.style.setProperty("box-shadow", `inset 6px 0 0 ${hex}`, "important");
    el.style.setProperty("outline", `1px solid ${hex}33`, "important");
    return stripe;
}

// ---- Main repaint logic ----
async function repaintContainer(container) {
    const model = "crm.lead"; // TEMP: force CRM; switch to auto-detect later
    const cards = Array.from(container.querySelectorAll(".o_kanban_record"));
    if (!cards.length) return;

    // Collect ids
    const ids = [];
    const byId = new Map();
    for (const el of cards) {
        const id = getResId(el);
        if (!id) continue;
        if (!byId.has(id)) {
            byId.set(id, el);
            ids.push(id);
        }
    }
    console.log("[OKC] ids to fetch:", ids);

    // Default paint so you see something instantly
    for (const el of cards) {
        if (!el.classList.contains("okc-card")) {
            el.classList.add("okc-card");
            ensureStripe(el, "#3b82f6");
        }
    }

    // Fetch metrics if we have ids
    let metrics = {};
    if (ids.length) {
        try {
            metrics = await rpc("/web/dataset/call_kw/kanban.metrics.mixin/get_kanban_metrics", {
                model: "kanban.metrics.mixin",
                method: "get_kanban_metrics",
                args: [model, ids],
                kwargs: {},
            });
            console.log("[OKC] metrics keys:", Object.keys(metrics || {}));
        } catch (e) {
            console.warn("[OKC] metrics RPC failed:", e);
        }
    }

    // Apply per card
    for (const el of cards) {
        const id = getResId(el);
        const m = (id && metrics) ? metrics[id] : null;

        el.classList.remove("okc-card--green", "okc-card--orange", "okc-card--red", "okc-card--blue");

        let chosen = colorFromMetrics(m);
        if (!chosen.cls) {
            chosen = colorFromColumn(el); // stage/column-based fallback
        }
        if (chosen.cls) el.classList.add(chosen.cls);
        ensureStripe(el, chosen.hex || "#9ca3af");

        // Counters (only if metrics exist)
        if (m && !el.querySelector(":scope > .okc-counters")) {
            const footer = document.createElement("div");
            footer.className = "okc-counters";
            footer.title = buildTooltip(m);
            const pills = [`A: ${m.activities_count ?? 0}`, `U: ${m.unread_count ?? 0}`];
            if (typeof m.subtask_count === "number") pills.push(`S: ${m.subtask_count}`);
            footer.innerHTML = pills.map(t => `<span class="okc-pill">${t}</span>`).join("");
            el.appendChild(footer);
        }
    }
}

function repaintAll() {
    document.querySelectorAll(".o_kanban_renderer").forEach(repaintContainer);
}

// ---- Boot service ----
registry.category("services").add("okc_painter", {
    start() {
        console.log("[OKC] painter service started (diagnostic+fallback)");
        repaintAll();
        setTimeout(repaintAll, 400);
        setTimeout(repaintAll, 1200);
        const obs = new MutationObserver((muts) => {
            if (muts.some(m => (m.addedNodes && m.addedNodes.length) || m.type === "childList")) repaintAll();
        });
        obs.observe(document.body, { childList: true, subtree: true });
        console.log("[OKC] observer installed");
    },
});
