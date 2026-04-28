from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = "pos.order"


    pos_order_type_id= fields.Many2one("pos.order.type",string="POS Order Type", readonly=True)