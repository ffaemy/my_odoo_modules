# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


