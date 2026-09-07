# models/kanban_metrics_mixin.py
from odoo import api, models, fields

class KanbanMetricsMixin(models.AbstractModel):
    _name = "kanban.metrics.mixin"
    _description = "Server helper to compute Kanban counters & status"

    @api.model
    def get_kanban_metrics(self, model, ids):
        ids = list(map(int, ids or []))
        if not ids or model not in ("crm.lead", "project.task"):
            return {}
        env = self.env[model].sudo()
        records = env.browse(ids)
        res, today = {}, fields.Date.context_today(self)

        for rec in records:
            deadline = getattr(rec, "date_deadline", None) or getattr(rec, "date", None)
            days_left = (deadline - today).days if deadline else None
            activities_count = getattr(rec, "activity_count", 0)
            unread_count = getattr(rec, "message_needaction_counter", 0)
            subtask_count = len(getattr(rec, "child_ids", [])) if rec._name == "project.task" else 0
            if rec._name == "project.task":
                stage = getattr(rec, "stage_id", False)
                is_done = bool(stage and getattr(stage, "is_closed", False))
            else:
                is_done = getattr(rec, "probability", 0) >= 100 or (
                    getattr(rec, "stage_id", False) and getattr(rec.stage_id, "is_won", False)
                )
            res[rec.id] = {
                "deadline_days_left": days_left,
                "activities_count": activities_count or 0,
                "unread_count": unread_count or 0,
                "subtask_count": subtask_count or 0,
                "is_done": is_done,
            }
        return res
