from odoo import models, fields, api,_

class AccountlabelValue(models.Model):
    _inherit="account.move"
    
    
    @api.onchange('line_ids' , 'ref')
    def get_label_val(self):
        for rec in self:
            if rec.ref:
                if rec.line_ids:
                    for line in rec.line_ids:
                        line.name= rec.ref
        
        
    
     
    
    





# class je_default_label(models.Model):
#     _inherit ="account.move.line"
#     
#     
#     
#     @api.onchange('move_id.ref')
#     def label_update(self):
#         for rec in self:
#             if rec.move_id.ref:
#                 lbl= rec.move_id.ref
#                 return lbl
    
    
#     name = fields.Char(string='Label', tracking=True, default=label_update)   
#     name = fields.Char(string='Label', tracking=True, default=lambda self:self.move_id.ref)       
#     @api.model
#     def default_get(self, fields):
#         res = super(je_default_label, self).default_get(fields)
#        
#         if self.move_id.ref:
#             res['name'] = self.move_id.ref
# 
#         return res
#     
    
    
#     @api.onchange('move_id.ref')
#     def get_label_value(self):
#         for rec in self:
#             if rec.move_id.ref:
#                 rec.name = rec.move_id.ref
        