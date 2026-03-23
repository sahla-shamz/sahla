# -*- coding: utf-8 -*-

from odoo import fields,models,api, _
from datetime import date

class MachineTransfer(models.Model):
    _name = 'machine.transfer'
    _description = 'Machine Transfer'
    _rec_name = "seq_number"
    _inherit = ["mail.thread"]
    _order= "transfer_states"

    machine_id=fields.Many2one("machine.management.machine",string="Machine",required=True)
    machine_serial_num=fields.Char("Serial Number", related="machine_id.sequence_number")
    transfer_date=fields.Date(string="Transfer Date", default= date.today())
    transfer_type=fields.Selection([('install','Install'), ('remove','Remove')],string="Transfer Type")
    customer_id=fields.Many2one("res.partner",string="Customer")
    internal_notes=fields.Text(string="Internal Notes")
    transfer_states=fields.Selection([('draft','Draft'), ('transfer','Transfer')],
                                     string="Transfer States",
                                     default='draft', tracking=True)
    machine_ids=fields.Many2many(comodel_name='machine.management.machine',
                                 string="Machine idss",
                                 compute='_compute_machine_ids',
                                 store=True)

    active=fields.Boolean(string="Active", default=True)
    seq_number= fields.Char(string="Sequence Number", default= lambda self: _('New'), readonly=True, copy=False)
    company_id=fields.Many2one("res.company",string="Company", default= lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['seq_number'] = self.env["ir.sequence"].next_by_code("machine.transfer")

        return super(MachineTransfer, self).create(vals_list)

    def transfer_action(self):
        """transfer action button in machine"""
        for record in self:
            if record:
                record.machine_id.write({'state':'in_service'})
                record.machine_id.write({'customer_id':record.customer_id})
                record.write({'transfer_states':'transfer'})


    @api.depends("transfer_type")
    def _compute_machine_ids(self):
        """show active machine when transfer type is 'install' and in_service machines when type is 'remove'"""
        all_records= self.machine_id.search([])
        for record in self:
            if ((record.machine_id.state == 'in_service' and record.transfer_type == 'install')
                    or (record.machine_id.state == 'active' and record.transfer_type == 'remove')):
                record.write({'machine_id': False})

            if record.transfer_type == 'install':
                self.update({
                    'machine_ids':[fields.Command.set(all_records.filtered(lambda s: s.state == 'active').ids)]
                })
            elif record.transfer_type == 'remove':
                self.update({
                    'machine_ids':[fields.Command.set(all_records.filtered(lambda s: s.state == 'in_service').ids)]
                })
            else:
                self.update({
                    'machine_ids':[fields.Command.set(all_records.ids)]
                })



                """LINK AND CLEAR"""

                # record.machine_ids= self.machine_id.search([('state','=','active')])

                # new=self.machine_id.search([('state','=','active')]).ids
                # if new:
                #     for r in new:
                #         self.update({
                #             'machine_ids':[fields.Command.link(r)]
                #         })
                #         print(self.machine_ids)
                # else:
                #     record.machine_ids=False

                # record.machine_ids = self.machine_id.search([('state','=','in_service')])
                # for r in self.machine_id.search([('state','=','in_service')]).ids:
                #
                #     self.update({
                #         'machine_ids':[fields.Command.link(r)]
                #     })
                #     print(self.machine_ids)

                # for r in self.machine_id.search([('state','=',['in_service','active'])]).ids:
                #
                #     self.update({
                #         'machine_ids':[fields.Command.link(r)]
                #     })
                #     print(self.machine_ids)

                # self.update({
                #     'machine_ids': [fields.Command.clear()]
                # })