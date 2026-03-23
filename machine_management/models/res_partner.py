from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = "res.partner"

    # new=fields.Char(string="Newww")
    machine_ids=fields.One2many("machine.management.machine","customer_id",string="Machine")
    machine_count=fields.Integer(string="Number of Machines", compute="_compute_machine_count", store=True)



    @api.depends('machine_ids')
    def _compute_machine_count(self):
        for record in self:
            record.machine_count = len(record.machine_ids)


    def action_archive(self):
        print("archive")
        print(self.machine_ids)
        self.machine_ids.action_archive()
        return super(ResPartner, self).action_archive()



    def action_unarchive(self):
        print("unarchive")
        for i in self:
            mac = self.machine_ids.search([('active','=',False), ('customer_id','in',i)])
            print("mac", mac)
            mac.action_unarchive()
        return super().action_unarchive()


    def action_customer_machines(self):
        return {
            'name': 'Machines',
            'type': 'ir.actions.act_window',
            'res_model': 'machine.management.machine',
            'view_mode': 'list,form',
            'domain' : [('customer_id' , 'in' , self.id)]
        }