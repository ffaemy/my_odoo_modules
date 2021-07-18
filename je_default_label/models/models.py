# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class je_default_label(models.Model):
#     _name = 'je_default_label.je_default_label'
#     _description = 'je_default_label.je_default_label'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
