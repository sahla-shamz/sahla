from email.policy import default

from odoo import fields, models, api, _
from datetime import date

class MachineService(models.Model):
    _name = 'machine.service'
    _description = 'Machine Service'
    _rec_name = 'seq_number'
    _inherit = "mail.thread"
    _order= 'service_state desc'

    machine_id=fields.Many2one("machine.management.machine", string="Machine Name")
    customer_id=fields.Many2one("res.partner", string="Customer", related="machine_id.customer_id", store=True)
    date=fields.Date(string="Date", default= date.today())
    description=fields.Text(string="Description")
    service_state=fields.Selection([('open','Open'), ('started','Started'),('done','Done'),('cancel','Cancel')],string="Service State", default="open", copy=False, tracking=True)
    company_id=fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    internal_note=fields.Text(string="Internal Note")
    tech_person_ids=fields.Many2many("res.users", string="Tech Person", default= lambda self: self.env.user)
    machine_parts_ids=fields.One2many("machine.parts","service_id",string="Machine Parts", compute="_compute_machine_parts")
    account_move_id=fields.Many2one("account.move",string="Account Move")
    account_line_id=fields.Many2one("account.move.line",string="Account Move")
    invoice_count = fields.Integer("Invoice Count", compute="_compute_invoice_count", store=True)
    invoice_ids = fields.One2many("account.move", "service_id", string="Invoices")
    is_invoiced= fields.Boolean(string="Is Invoiced", default= False)
    seq_number= fields.Char(string="Sequence Number", default= lambda self: _('New'), readonly=True, copy=False)


    @api.model_create_multi
    def create(self, vals_list):
        """Create  a sequence number for Service"""
        for vals in vals_list:
            if vals.get("seq_number", _('New')==_('New')):
                vals["seq_number"]= self.env["ir.sequence"].next_by_code('machine.service')

            return super(MachineService, self).create(vals_list)


    @api.depends("machine_id.machine_parts_ids")
    def _compute_invoice_products(self):
        for record in self:
            record.account_move_id.invoice_line_ids = record.machine_id.machine_parts_ids


    @api.depends('machine_id.machine_parts_ids')
    def _compute_machine_parts(self):
        for record in self:
            record.machine_parts_ids = record.machine_id.machine_parts_ids


    def start_action(self):
        """Start button action on the service form"""
        for record in self:
            record.write({'service_state' : 'started'})

    def close_action(self):
        """Close button action and sends an email"""
        for record in self:
            record.write({'service_state': 'done'})
            template = self.env.ref('machine_management.email_template_name')
            template.send_mail(self.id, force_send=True)
            record.machine_id.last_service_date= record.date


    def cancel_action(self):
        """Cancel button action"""
        for record in self:
            record.write({'service_state' : 'cancel'})



    def create_invoice(self):
        """Create invoice button action"""
        for record in self:
            record.write({'is_invoiced' : 'True'})
            invoice= self.env['account.move'].search([('partner_id', '=', record.customer_id.id),('move_type','=','out_invoice'), ('state', '=','draft')], limit=1)

            if not invoice:
                invoice=self.env['account.move'].create({
                    'partner_id': record.customer_id.id,
                    'move_type':'out_invoice',
                    'state':'draft',
                })

            self.write({'account_move_id' : invoice.id})
            invoice.write({'service_id' :  record.id})

            for rec in record.machine_parts_ids:
                self.env["account.move.line"].create({
                'move_id': invoice.id,
                'partner_id': record.customer_id.id,
                'product_id': rec.product_id.id,
                'product_uom_id': rec.uom_id.id,
                'quantity': rec.quantity,
                'price_unit': rec.price_unit,
                })


        prod_id = self.env.ref("machine_management.product_invoice")

        if prod_id.id not in invoice.invoice_line_ids.mapped('product_id.id'):
            self.env['account.move.line'].create({
                'product_id': prod_id.id,
                'move_id': invoice.id
            })

        return{
            'name': 'Invoice',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': invoice.id,
            }


    def action_view_invoice(self):
        """View Invoice smart button"""
        return {
            "name" : "View Invoice",
            "res_model" : "account.move",
            "type" : "ir.actions.act_window",
            "view_mode" : "list,form",
            "domain": [("service_id", '=', self.id)]
        }

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """Count the number of invoices"""
        for record in self:
            record.invoice_count = len(record.invoice_ids)


