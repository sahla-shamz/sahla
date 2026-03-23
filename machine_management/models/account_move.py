from odoo import fields, models,api

class AccountMove(models.Model):
    _inherit = 'account.move'

    service_id=fields.Many2one("machine.service",string="service")




