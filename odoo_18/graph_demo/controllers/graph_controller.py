from odoo import http
from odoo.http import request
import matplotlib.pyplot as plt
import io
import base64

class GraphController(http.Controller):
    @http.route('/graph_demo/graph', type='http', auth='public', website=True)
    def generate_graph(self, **kwargs):
        records = request.env['graph.demo'].sudo().search([], order="date asc")

        # Use dates as labels and their corresponding values
        dates = [rec.date.strftime("%Y-%m-%d") for rec in records]
        values = [rec.value for rec in records]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(dates, values, color='skyblue')
        ax.set_title("Dynamic Graph from Odoo Model")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        plt.xticks(rotation=45)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        plt.close(fig)  # Close plot to free memory

        return request.render('graph_demo.graph_template', {'graph_img': image_base64})
