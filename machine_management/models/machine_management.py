# -*- coding: utf-8 -*-

from odoo import fields,_, models, api
from odoo.exceptions import ValidationError, UserError, RedirectWarning, AccessError
from datetime import date, datetime
from odoo import Command

from odoo.tools import date_utils


class MachineManagement(models.Model):
    _name= 'machine.management.machine'
    _description=  "Machine Management"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _rec_name = "name"
    _order = "state"

    name= fields.Char(string="Name", required=True, tracking=True, copy=False)
    date_of_purchase= fields.Date(string="Date of purchase", default=date.today())
    purchase_value=fields.Monetary(string="Purchase Value", currency_field="currency_id")
    company_id=fields.Many2one(comodel_name='res.company', string="Company", default=lambda self: self.env.company)
    currency_id=fields.Many2one("res.currency", string="Currency", default= lambda self:self.env.user.company_id.currency_id)
    customer_id=fields.Many2one("res.partner",string="Customer", readonly=True)
    state=fields.Selection([('active', 'Active'), ('in_service', 'In Service'),],string="State", default="active", copy=False, tracking=True)
    description=fields.Text(string="Description")
    image=fields.Image(string="Image")
    is_warranty= fields.Boolean(string="Warranty")
    machine_instructions=fields.Html(string="Machine Instructions")
    sequence_number= fields.Char(string="Sequence Number", readonly=True,default=lambda self: _('New'),copy=False, tracking=True)
    machine_type= fields.Many2one('machine.type',string="Machine Type")
    transfer_count=fields.Integer(string="Transfer Count", compute="_compute_transfer_count", store=True, copy=False)
    transfer_ids=fields.One2many(comodel_name='machine.transfer',inverse_name='machine_id',string="Transfers")
    serial_no=fields.Char(string='Serial No')
    machine_parts_ids=fields.One2many(comodel_name='machine.parts',inverse_name='machine_id',string="Machine Parts")
    machine_tags=fields.Many2many(comodel_name='machine.tags',string="Machine Tags")
    machine_age= fields.Integer(string="Machine Age", compute="_compute_age")
    total= fields.Float(string="Total", compute='_compute_total')
    terms=fields.Text(string="Terms and conditions")
    service_ids=fields.One2many("machine.service","machine_id",string="Service")
    service_count= fields.Integer(string="Service Count", compute="_compute_service_count", store=True)
    active= fields.Boolean("Active", default=True)
    last_service_date = fields.Date(string="Last Service Date", default=date.today(), readonly=True)
    todays_date= fields.Date(string="Todays Date", default= date.today())
    next_service_date= fields.Date(string="Next Service Date", default=date.today(), compute="_compute_next_service_date", store=True)
    service_frequency= fields.Selection([('weekly', 'Weekly'),('monthly',' Monthly'), ('yearly','Yearly')])


    sale_order_id= fields.Many2one("sale.order", string="Sale Order")


    _unique_serial_no = models.Constraint(
        'UNIQUE(serial_no)',
        'Serial number should be unique',
    )


    @api.depends("last_service_date")
    def _compute_next_service_date(self):
        """Compute the next service date"""
        for record in self:
            if record.service_frequency == 'monthly':
                record.next_service_date = date_utils.add(self.last_service_date, months=1)

            elif record.service_frequency == 'weekly':
                record.next_service_date = date_utils.add(self.last_service_date, days=7)

            else:
                record.next_service_date = date_utils.add(self.last_service_date, years=1)


    def unlink(self):
        """machine with transfers cannot be deleted"""
        for record in self:
            if record.transfer_count >= 1:
                raise UserError("Machine with transfers cannot be deleted")

        return super().unlink()


    @api.depends("date_of_purchase")
    def _compute_age(self):
        """Calculate the age of the machine"""
        for record in self:
            record.machine_age= (date.today() - record.date_of_purchase).days
            print(record.machine_age)


    @api.model_create_multi
    def create(self, vals_list):
        """creating the sequence number for each machine"""
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = self.env['ir.sequence'].next_by_code('machine.management.machine')
        return super().create(vals_list)


    @api.constrains("purchase_value")
    def _check_purchase_value(self):
        """Validating the purchase value of the machine"""
        for record in self:
            if record.purchase_value <= 0:
                raise ValidationError("Purchase value must be greater than 0")


    @api.depends("transfer_ids")
    def _compute_transfer_count(self):
        """Computing the total transfer count of the machine"""
        for record in self:
            record.transfer_count=len(record.transfer_ids)


    def go_to_transfer_action(self):
        """create transfer from machine page"""
        return {
            'name': 'Transfer',
            'view_mode': 'form',
            'res_model': 'machine.transfer',
            'type': 'ir.actions.act_window',
            'context': {'default_machine_id': self.id}
        }


    def transfers_action(self):
        """Transfer smart button which shows all the transfers of the machine"""
        return{
            'name': 'Transfer smart Button',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'machine.transfer',
            'domain': [('machine_id', '=', self.id)]
        }


    @api.depends('machine_parts_ids.amount')
    def _compute_total(self):
        """Compute the total Amount"""
        for record in self:
            if record.mapped('machine_parts_ids.product_id'):
                for a in record.mapped('machine_parts_ids.amount'):
                    record.total += a
            else:
                record.total = 0



    def create_service_action(self):
        """Create Service button action"""
        return {
            "name" : "Create Service",
            "res_model" : "machine.service",
            "type" : "ir.actions.act_window",
            'context' : {'default_machine_id': self.id},
            "view_mode" : "form"
        }

    def service_action(self):
        """Services smart button"""
        return {
            "name" : "List Service",
            "res_model" : "machine.service",
            "type" : "ir.actions.act_window",
            'view_mode' : 'list,form',
            'domain': [('machine_id', '=', self.id)]
        }

    @api.depends('service_ids')
    def _compute_service_count(self):
        """Compute the total number of services in the machine"""
        for record in self:
            record.service_count= len(record.service_ids)


    def action_archive(self):
        if not self.env.user.has_group('machine_management.res_user_group_machine_manager'):
            raise AccessError("You have no permission to archive. Please contact the Manager")
        else:
            open_services= self.service_ids.filtered(lambda i :i.service_state=='open')
            print(open_services)
            for record in self:
                if record.state == 'active':
                    if open_services:
                        print("open services")
                        open_services.write({'service_state':'cancel'})
                    self.transfer_ids.action_archive()
                    res= super().action_archive()
                    if open_services:
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Warning!',
                                'message': 'Services are cancelled',
                                'type': 'success',
                                'sticky': False,
                                'next': {'type': 'ir.actions.act_window_close'},
                            }
                        }


                else:
                    raise UserError(_("You are not allowed to archive in Service Machines"))
                return res


    def action_unarchive(self):
        for i in self:
            transfers= i.transfer_ids.search([('active', '=', 'False'), ('machine_id', '=', i)])
            transfers.action_unarchive()
            res= super().action_unarchive()
        return res



    @api.model
    def recurrent_services(self):
        machines= self.env['machine.management.machine'].search([])
        for machine in machines:
            if machine.state == 'in_service' and machine.todays_date == machine.next_service_date:
                for i in machine.service_ids:
                    opened_services= False
                    if i.service_state != 'done':
                        opened_services= True
                        break

                if not machine.service_ids or not opened_services:
                     machine.service_ids.create({
                                            'machine_id': machine.id,
                                            'customer_id': machine.customer_id.id,
                                            'date' : machine.next_service_date,
                                            'machine_parts_ids':[Command.create({
                                    'product_id': i.product_id,
                                     'quantity': i.quantity,
                                     'uom_id': i.uom_id.id,
                                     'price_unit': i.price_unit,
                                     'amount': i.amount,
                        }) for i in machine.machine_parts_ids]
                                        })






    def sale_order_action(self):
        print("saleeeee")
        print("########################################")

        print(self.machine_parts_ids.product_id)
        print("######################################333")
        for record in self:
            print("customer::", record.sale_order_id.partner_id.name)
            print("Total sale order Count::", record.sale_order_id.partner_id.sale_order_count)
            print("total Sale order Amount::",sum(record.sale_order_id.partner_id.sale_order_ids.mapped("amount_total")))
            dict = {}
            for i in record.sale_order_id.partner_id.sale_order_ids:
                for product in i.order_line:
                    # print("product Name",product.product_template_id.name)
                    # print("product quantity",product.product_uom_qty)
                    if product.product_template_id.name not in dict:
                        dict[product.product_template_id.name] = product.product_uom_qty
                    else:
                        dict[product.product_template_id.name] += product.product_uom_qty
                    # print(dict)
        print(dict)

        m= sorted(dict.items(), key=lambda arg: arg[-1])
        print(m)

        print("Leastt", m[0])
        print("Most", m[-1])


        # l=[]
        # for i,j in dict.items():
        #     l.append(j)
        #
        # for i,j in dict.items():
        #     if max(l)==j:
        #         print("Top selling Product and Quantity::",i,j)
        #
        #     if min(l)==j:
        #         print("Least selling Product and Quantity::",i,j)


        s = self.sale_order_id.partner_id.sale_order_ids.filtered(lambda l: l.date_order.month == 2)
        # print(s)
        print("Current month Sales Total::",sum(s.mapped('amount_total')))




