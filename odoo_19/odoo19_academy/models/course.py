# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AcademyCourse(models.Model):
    _name = "academy.course"
    _description = "Academy Course"
    _order = "name"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    responsible_id = fields.Many2one("res.users", string="Responsible")
    credits = fields.Integer("Credits", default=3)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("name_unique", "unique(name)", "Course title must be unique."),
    ]

    @api.constrains("credits")
    def _check_credits(self):
        for rec in self:
            if rec.credits < 0:
                raise ValueError("Credits cannot be negative.")
