from odoo import http
from odoo.http import request, content_disposition
from werkzeug.exceptions import NotFound


class PdfdTemplateExportController(http.Controller):
    @http.route(
        "/pdfd_lite/export/<int:template_id>",
        type="http",
        auth="user",
        methods=["GET"],
        csrf=False,
    )
    def export_template_xml(self, template_id, **kwargs):
        template = request.env["pdfd.template"].browse(template_id)
        if not template.exists():
            raise NotFound()

        # Always ensure we have fresh XML before exporting.
        if not template.xml_arch:
            template.action_generate_xml()

        tname = template._normalized_tname()
        filename = f"{tname.replace('.', '_')}.xml"

        headers = [
            ("Content-Type", "application/xml; charset=utf-8"),
            ("Content-Disposition", content_disposition(filename)),
        ]
        return request.make_response((template.xml_arch or "").encode("utf-8"), headers)