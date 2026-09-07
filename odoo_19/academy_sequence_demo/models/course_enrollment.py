from odoo import api, fields, models


class CourseEnrollment(models.Model):
    _name = "academy.course.enrollment"
    _description = "Course Enrollment (Demo)"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        default="New",
        required=True,
        readonly=True,
        copy=False,
        index=True,
    )
    student_name = fields.Char(string="Student Name", required=True)
    course_name = fields.Char(string="Course Name")
    enrollment_date = fields.Date(
        string="Enrollment Date", default=fields.Date.context_today
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"]
                    .next_by_code("academy.course.enrollment")
                    or "New"
                )
        return super().create(vals_list)
