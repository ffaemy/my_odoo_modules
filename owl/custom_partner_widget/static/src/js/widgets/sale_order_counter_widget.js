/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class SaleOrderCounterWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ count: 0 });
        onWillStart(async () => {
            const res = await this.orm.read("res.partner", [this.props.record.res_id], ["sale_order_count"]);
            this.state.count = res[0]?.sale_order_count || 0;
        });
    }
}
SaleOrderCounterWidget.template = "custom_partner_widget.SaleOrderCounter";

registry.category("field_widgets").add("sale_order_counter", SaleOrderCounterWidget);
