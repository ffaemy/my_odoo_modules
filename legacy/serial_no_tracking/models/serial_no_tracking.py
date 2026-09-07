from odoo import models, fields, api
from re import findall as regex_findall
from re import split as regex_split

class serial_no_tracking(models.Model):
    _inherit="stock.move"
    
    serial_lot_check = fields.Boolean(string='serial lot check', default= False)
    tarcking_starting_no = fields.Many2one('stock.production.lot', string="Serial no starts from")
    
    
    
    def get_next_serial(self , serial_no):
        next_serial_no = ''
        caught_initial_number = regex_findall("\d+", serial_no)
        initial_number = caught_initial_number[-1]
        padding = len(initial_number)
        splitted = regex_split(initial_number, serial_no)
        prefix = initial_number.join(splitted[:-1])
        suffix = splitted[-1]
        initial_number = int(initial_number)
        new_serial = prefix +  str(int(initial_number) + 1).zfill(padding) +suffix
        next_serial_no = new_serial
        
        return next_serial_no
        
    
    
    
    
    def get_global_serial_no(self , rec):
        prev_serial_no = self.env['stock.production.lot'].search([('global_tracking','=',True)])
        
        stock_rec =  self.env['stock.move'].search([('id','in',[i.id for i in rec])])
        newly_created = stock_rec[0].picking_id.move_line_ids.mapped('lot_name') 
        newly_created =[nc for nc in newly_created if nc != False]
        
        if len(newly_created) != 0:
            serial_lot_name = newly_created[-1]
            
        else:
            if prev_serial_no:
                serial_lot_name =  prev_serial_no[-1].name
                
            
        if prev_serial_no or len(newly_created) != 0:
#             stock_rec =  self.env['stock.move'].search([('id','in',[i.id for i in rec])])
#             stock_rec.serial_lot_check = True
            first_rec_flag = False
            
            for record in stock_rec:
                if first_rec_flag == False:
                     
                    record.update({'serial_lot_check':True})
                    new_serial = self.get_next_serial(serial_lot_name)
                    record.next_serial = new_serial
                    product_count=0.0
                    if record.product_uom_qty:
                        product_count = int(record.product_uom_qty)
                    record._generate_serial_numbers(product_count)
                    first_rec_flag =True
                    
                elif first_rec_flag == True:
                    record.update({'serial_lot_check':True})
                    prev_tracking_no_list = stock_rec.move_line_ids.mapped('lot_name')
                    prev_serial_name = [x for x in prev_tracking_no_list if x!= False]
                    
                    if prev_serial_name:
                        new_serial = self.get_next_serial(prev_serial_name[-1])
                        record.next_serial = new_serial
                        product_count=0.0
                        if record.product_uom_qty:
                            product_count = int(record.product_uom_qty)
                        record._generate_serial_numbers(product_count)
                        
    
    
    
    def action_show_details(self):
        res= super(serial_no_tracking,self).action_show_details()
        if self.picking_id.purchase_id:
            print(self.picking_id.purchase_id)
            prev_serial_no = self.env['stock.production.lot'].search([('global_tracking','=',True)])
            print(prev_serial_no)
    
            if prev_serial_no:
                stock_rec=  self.env['stock.move'].search([('id','=',res['res_id'])])
                if stock_rec.product_id.product_tmpl_id.tracking != 'none': 
                    stock_rec.serial_lot_check = True
                    prev_serial_no =prev_serial_no[-1]
    #         
                    new_serial = self.get_next_serial(prev_serial_no.name)
                    res['context']['next_serial'] = new_serial
                    stock_rec.next_serial = new_serial
                    stock_rec._generate_serial_numbers()

        return res
        

class RemoveCreateEditButton(models.Model):
    _inherit = 'stock.picking'
    
#     tarcking_starting_no = fields.Many2one('stock.production.lot', string="Serial no starts from")
#     so_delivry=fields.Boolean('SO Delivery', default=False , copy=False, compute="domain_picking")
#     
#     
#     @api.onchange('picking_type_id')
#     def visibilty_of_tracking_field(self):
#         if self.picking_type_id:
#             if (self.picking_type_id.code == 'outgoing'):
#                 self.update({'so_delivry' : True })
#             elif (self.picking_type_id.code != 'outgoing'):
#                 self.update({'so_delivry' : False }) 
#                 
#     @api.depends('picking_type_id')
#     def domain_picking(self):
#         for rec in self:
# #             if (rec.state not in ['draft', 'confirmed', 'waiting']):
#             if (rec.picking_type_id.code == 'outgoing'):
#                 rec.so_delivry = True
#             else:
#                  rec.so_delivry = False
#     
    def button_validate(self): 
        if self.purchase_id:
            if self.move_lines:
                trackable_prod_lines = self.move_lines.filtered(lambda r:r.product_id.product_tmpl_id.tracking !='none')
                if trackable_prod_lines:
                    trackable_lines=[]
                    for tr_ln in trackable_prod_lines:
                        lot_name = tr_ln.mapped('move_line_ids.lot_name')
                        lot_name_exist=[x for x in lot_name if x != False]
                        lot_id_exist = tr_ln.move_line_ids.mapped('lot_id')
                        if not lot_name_exist and not lot_id_exist:
                            trackable_lines.append(tr_ln)
                            
                    if  len(trackable_lines) >= 1:   
                        self.env['stock.move'].get_global_serial_no(trackable_lines)    
                    
            
            

#                        
                    
                
                    
        res= super(RemoveCreateEditButton,self).button_validate()
        if res == True and self.sale_id:
            if self.move_lines and self.move_lines.lot_ids:
                self.move_lines.lot_ids.update({'product_used': True})
                
        s=''
        return res


    def action_assign_tracking(self):
        action = self.env["ir.actions.actions"]._for_xml_id("serial_no_tracking.action_assign_tracking_wizard_view")
        return action        

class GlobalSerialLot(models.Model):
    _inherit="stock.production.lot"
    
    
    global_tracking = fields.Boolean(stirng='Global Tracking', default=False) 
    product_used = fields.Boolean(stirng ='Used', default=False , readonly = True)


class StockMoveGlobalTracking(models.Model):
    _inherit="stock.move.line"
    
    
    
    
    
    def _create_and_assign_production_lot(self):
       """ Creates and assign new production lots for move lines."""
       lot_vals = [{
            'company_id': ml.move_id.company_id.id,
            'name': ml.lot_name,
            'global_tracking':True,
            'product_id': ml.product_id.id,
        } for ml in self]
       lots = self.env['stock.production.lot'].create(lot_vals)
       for ml, lot in zip(self, lots):
           ml._assign_production_lot(lot)


