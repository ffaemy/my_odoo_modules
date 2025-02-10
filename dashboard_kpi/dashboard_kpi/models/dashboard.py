from odoo import models, fields, api

class SalesInventoryDashboard(models.Model):
    _name = "custom.kpi.dashboard"
    _description = "Custom KPI Dashboard for Sales & Inventory"
    
    total_sales = fields.Float(string="Total Sales")
    total_orders = fields.Integer(string="Total Orders")
    total_stock = fields.Float(string="Total Stock")

    def action_refresh_dashboard(self):
        """ Manually refresh KPI values """
        for record in self:
            record.total_sales = sum(self.env["sale.order"].search([("state", "=", "sale")]).mapped("amount_total"))
            record.total_orders = self.env["sale.order"].search_count([("state", "=", "sale")])
            
            # Fetch total available stock using _compute_quantities_dict()
            products = self.env["product.product"].search([])
            stock_data = products._compute_quantities_dict(None, None, None)
            record.total_stock = sum(stock_data[p.id]["qty_available"] for p in products)
            
            print("Dashboard Updated - Total Sales:", record.total_sales)
            print("Dashboard Updated - Total Orders:", record.total_orders)
            print("Dashboard Updated - Total Stock:", record.total_stock)
