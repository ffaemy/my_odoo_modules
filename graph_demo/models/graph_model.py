from odoo import models, fields, api

class GraphDemo(models.Model):
    _name = 'graph.demo'
    _description = 'Graph Demo Data'
    
    name = fields.Char(string='Category', required=True)
    value = fields.Float(string='Value', required=True)
    date = fields.Date(string='Date', required=True)
