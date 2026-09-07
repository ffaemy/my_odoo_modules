from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PdfdTemplate(models.Model):
    _name = 'pdfd.template'
    _description = 'PDF Designer Lite Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True, tracking=True)
    key = fields.Char(string='QWeb t-name', help='Used as <t t-name="...">', copy=False)


    # Simple switches instead of a builder UI
    show_logo = fields.Boolean(default=True)
    title_text = fields.Char(default='Document Title')
    title_align = fields.Selection([('left','Left'),('center','Center'),('right','Right')], default='center')
    show_header_fields = fields.Boolean(string='Show Customer & Number', default=True)
    show_table = fields.Boolean(default=True)
    show_totals = fields.Boolean(default=True)
    footer_text = fields.Char(string='Footer Text', default='Thank you for your business!')


    # Generated XML + Preview
    xml_arch = fields.Text(readonly=True)
    preview_html = fields.Html(sanitize=False, readonly=True)


    # Sample context for preview only
    sample_context = fields.Json(default=lambda self: {
    'company': {'name': 'Odooistic Ltd', 'logo': '/web/static/img/placeholder.png'},
    'doc': {'name': 'John Carter', 'number': 'SO019', 'date_order': '2025-10-29', 'amount_total': 199},
    'lines': [
    {'name':'Monthly Membership','qty':1,'price_unit':49,'subtotal':49},
    {'name':'Personal Training (4x)','qty':1,'price_unit':150,'subtotal':150},
    ],
    'totals': {'untaxed':199,'tax':0,'total':199},
    })



    def _normalized_tname(self):
        import re
        base = (self.key or f'pdfd_lite_{self.id or "new"}').strip()
        base = re.sub(r'[^A-Za-z0-9._-]', '_', base)
        # If user typed a simple name, namespace it to avoid collisions
        if '.' not in base:
            base = f'odoo_pdf_designer_lite.{base}'
        return base
    
    def action_generate_xml(self):
        for rec in self:
            tname = rec._normalized_tname()
            pieces = [
                f'<t t-name="{tname}">',
                '<div class="doc">'
            ]

            # ✅ Safe logo expression for dict-based context
            if rec.show_logo:
                pieces.append(
                    '<div class="logo">'
                    '<img t-att-src="company and company.get(\'logo\')" style="max-height:64px"/>'
                    '</div>'
                )

            # Title
            if rec.title_text:
                pieces.append(
                    f'<h2 style="text-align:{rec.title_align}">{rec.title_text}</h2>'
                )

            # Header fields
            if rec.show_header_fields:
                pieces.extend([
                    "<div><strong>Customer:</strong> <span t-esc=\"doc.get('name')\"/></div>",
                    "<div><strong>Number:</strong> <span t-esc=\"doc.get('number')\"/></div>",
                ])

            # Table
            if rec.show_table:
                pieces.append('''
                    <table class="table table-sm" style="width:100%;border-collapse:collapse" border="1" cellpadding="6">
                        <thead>
                            <tr>
                                <th>Item</th><th>Qty</th><th>Price</th><th>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="lines" t-as="l">
                                <tr>
                                    <td><t t-esc="l.get('name')"/></td>
                                    <td><t t-esc="l.get('qty')"/></td>
                                    <td><t t-esc="l.get('price_unit')"/></td>
                                    <td><t t-esc="l.get('subtotal')"/></td>
                                </tr>
                            </t>
                        </tbody>
                    </table>
                ''')

            # Totals
            if rec.show_totals:
                pieces.append('''
                    <div class="totals" style="margin-top:10px">
                        <div>Untaxed: <span t-esc="totals.get('untaxed')"/></div>
                        <div>Tax: <span t-esc="totals.get('tax')"/></div>
                        <div><strong>Total: <span t-esc="totals.get('total')"/></strong></div>
                    </div>
                ''')

            # Footer
            if rec.footer_text:
                pieces.append(
                    f'<div class="footer" style="margin-top:16px;font-size:12px;color:#777">{rec.footer_text}</div>'
                )

            # Close tags
            pieces.append('</div></t>')

            # Save and render
            rec.xml_arch = "\n".join(pieces)
            rec.preview_html = rec._render_preview(tname)

    
    def _render_preview(self, tname=None):
        """Render xml_arch preview safely in Odoo 19."""
        self.ensure_one()
        from odoo import tools

        View = self.env["ir.ui.view"]
        tname = tname or self._normalized_tname()
        arch = self.xml_arch or f'<t t-name="{tname}"/>'

        # Give the transient view its own unique key
        view_key = f"odoo_pdf_designer_lite.preview_{self.id}"

        try:
            # Create the transient view record
            view = View.create({
                "name": f"PDFD Preview {self.id}",
                "type": "qweb",
                "arch_db": arch,
                "key": view_key,
            })

            # Clear caches so Odoo reindexes this transient view
            if hasattr(View, "clear_caches"):
                View.clear_caches()

            # ✅ Render by KEY (which is guaranteed to exist)
            html = View._render_template(view_key, self.sample_context or {})
            return html

        except Exception as e:
            return f"<div style='color:red;padding:1em;'>Preview failed: {tools.html_escape(str(e))}</div>"

        finally:
            # Cleanup transient view
            try:
                view.sudo().unlink()
            except Exception:
                pass

    def action_export_xml(self): 
        self.ensure_one() 
        return { 
            'type': 'ir.actions.act_url', 
            'url': f"/pdfd_lite/export/{self.id}", 
            'target': 'self', }