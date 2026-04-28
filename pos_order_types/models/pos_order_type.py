from odoo import api, fields, models

class OrderType(models.Model):
    _name = "pos.order.type"
    _description = "POS Order Type"
    _inherit = ['pos.load.mixin']


    name= fields.Char(string="Order Type", required=True)

