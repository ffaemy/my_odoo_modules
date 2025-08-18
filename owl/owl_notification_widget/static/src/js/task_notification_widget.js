/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

export class TaskNotificationWidget extends Component {
    setup() {
        this.state = useState({ tasks: [] });

        // Bind method to ensure `this` is correct in the template
        this.openTask = this.openTask.bind(this);

        onMounted(() => {
            this.refreshTasks();
            this.interval = setInterval(() => this.refreshTasks(), 15000);
        });

        onWillUnmount(() => {
            clearInterval(this.interval);
        });
    }

    async refreshTasks() {
        try {
            const result = await rpc("/task_notification/tasks");
            this.state.tasks = result;
        } catch (e) {
            console.error("❌ Failed to fetch tasks:", e);
        }
    }

    openTask(taskId) {
        if (!taskId) return;
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.task",
            res_id: taskId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

TaskNotificationWidget.template = "owl_notification_widget.TaskNotificationWidget";

registry.category("systray").add("task_notification_widget", {
    Component: TaskNotificationWidget,
});
